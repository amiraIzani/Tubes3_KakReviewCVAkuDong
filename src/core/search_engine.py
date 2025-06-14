import time
from collections import defaultdict

# --- Utility, Core, and Model Imports ---
# Assumes you have file_handler in a utils folder
from utils.file_handler import get_cv_path
from core.pdf_to_text import extract_text_from_pdf
from core.string_matcher import kmp_search, boyer_moore_search, levenshtein_distance
from core.regex import extract_all_cv_details
from model.models import fetch_applicant_by_id, fetch_all_cv_details as fetch_all_cv_application_details

# --- Algorithm Imports ---
from algorithms.kmp import KMP
from algorithms.bm import BoyerMoore
from algorithms.aho_corasick import AhoCorasick
from algorithms.levenshtein import calculate_levenshtein_similarity

# --- Configuration ---
DEFAULT_LEVENSHTEIN_SIMILARITY_THRESHOLD = 0.8
FREQUENCY_BONUS_WEIGHT = 0.01


def parse_keywords(keywords_str: str) -> list[str]:
    if not keywords_str:
        return []
    return [kw.strip().lower() for kw in keywords_str.split(",") if kw.strip()]

def perform_search(
        keywords_str: str,
        algorithm_choice: str,
        top_n: int,
        levenshtein_similarity_threshold: float = DEFAULT_LEVENSHTEIN_SIMILARITY_THRESHOLD
) -> tuple[list[dict], dict[str, float | str]]:
    
    total_timer_start = time.perf_counter()
    
    input_keywords = parse_keywords(keywords_str)
    
    if not input_keywords:
        return [], {'status_message': "No keywords provided.", 'total_processing_time': 0}

    all_cv_applications = fetch_all_cv_application_details()
    if not all_cv_applications:
        return [], {'status_message': "No CVs found in the database.", 'total_processing_time': 0}

    # Prepare CV data and pre-extract all text
    cv_data_for_processing = []
    cv_texts = {}
    applicant_cache = {}
    for app_detail_row in all_cv_applications:
        applicant_id = app_detail_row[1]
        cv_path_from_db = app_detail_row[3]

        if applicant_id not in applicant_cache:
            profile = fetch_applicant_by_id(applicant_id)
            name = "Unnamed Applicant"
            if profile:
                first_name, last_name = profile.get("first_name", ""), profile.get("last_name", "")
                name = f"{first_name} {last_name}".strip() or "Unnamed Applicant"
            applicant_cache[applicant_id] = name
        
        full_cv_path = get_cv_path(cv_path_from_db)
        if full_cv_path:
            cv_data_for_processing.append({
                'applicant_id': applicant_id, 'detail_id': app_detail_row[0],
                'name': applicant_cache[applicant_id], 'cv_path': cv_path_from_db,
            })
            _, pm_text = extract_text_from_pdf(full_cv_path)
            cv_texts[applicant_id] = {'pm': (pm_text or "").lower()}

    # This dictionary will hold all match data before final scoring
    results_in_progress = {}
    
    # --- EXACT MATCHING ---
    exact_timer_start = time.perf_counter()

    # AHO-CORASICK LOGIC
    if algorithm_choice.upper() == "AC":
        # Build the automaton once with all keywords
        automaton = AhoCorasick(input_keywords)
        for cv_info in cv_data_for_processing:
            applicant_id = cv_info['applicant_id']
            cv_pm_text = cv_texts.get(applicant_id, {}).get('pm', '')
            if not cv_pm_text: continue
            
            # Search once per CV, get all keyword matches
            found_keywords = automaton.search(cv_pm_text)
            if found_keywords:
                # Convert the result to the same format as our other algorithms
                matched_details = {kw: len(indices) for kw, indices in found_keywords.items()}
                results_in_progress[applicant_id] = {
                    'applicant_id': applicant_id, 'detail_id': cv_info['detail_id'],
                    'name': cv_info['name'], 'cv_path': cv_info['cv_path'],
                    'matched_keywords_details': defaultdict(int, matched_details)
                }

    # KMP / BOYER-MOORE LOGIC
    else:
        SearcherClass = KMP if algorithm_choice.upper() == "KMP" else BoyerMoore
        for cv_info in cv_data_for_processing:
            applicant_id = cv_info['applicant_id']
            cv_pm_text = cv_texts.get(applicant_id, {}).get('pm', '')
            if not cv_pm_text: continue

            matched_details = defaultdict(int)
            for keyword in input_keywords:
                searcher = SearcherClass(keyword)
                occurrences = searcher.search(cv_pm_text)
                if occurrences:
                    matched_details[keyword] = len(occurrences)
            
            if matched_details:
                results_in_progress[applicant_id] = {
                    'applicant_id': applicant_id, 'detail_id': cv_info['detail_id'],
                    'name': cv_info['name'], 'cv_path': cv_info['cv_path'],
                    'matched_keywords_details': matched_details
                }
    
    exact_match_duration = time.perf_counter() - exact_timer_start

    # FUZZY MATCHING
    fuzzy_timer_start = time.perf_counter()
    fuzzy_match_performed = False

    for cv_info in cv_data_for_processing:
        applicant_id = cv_info['applicant_id']
        current_result = results_in_progress.get(applicant_id)
        
        exact_matches = set(current_result['matched_keywords_details'].keys()) if current_result else set()
        unmatched_keywords = set(input_keywords) - exact_matches
        if not unmatched_keywords: continue

        cv_words = cv_texts.get(applicant_id, {}).get('pm', '').split()
        if not cv_words: continue

        for keyword in unmatched_keywords:
            best_similarity = 0.0
            for word in cv_words:
                similarity = calculate_levenshtein_similarity(keyword, word)
                if similarity >= levenshtein_similarity_threshold and similarity > best_similarity:
                    best_similarity = similarity
            
            if best_similarity > 0:
                fuzzy_match_performed = True
                fuzzy_key = f"{keyword} (fuzzy ~{int(best_similarity*100)}%)"

                if applicant_id not in results_in_progress:
                    results_in_progress[applicant_id] = {
                        'applicant_id': applicant_id, 'detail_id': cv_info['detail_id'],
                        'name': cv_info['name'], 'cv_path': cv_info['cv_path'],
                        'matched_keywords_details': defaultdict(float)
                    }
                
                # Store the similarity score as the value for the fuzzy match
                results_in_progress[applicant_id]['matched_keywords_details'][fuzzy_key] = best_similarity
    
    fuzzy_match_duration = (time.perf_counter() - fuzzy_timer_start) if fuzzy_match_performed else 0.0

    # FINAL SCORING & RANKING
    final_results = list(results_in_progress.values())

    for result in final_results:
        details = result['matched_keywords_details']
        
        exact_matches = {k: v for k, v in details.items() if not k.endswith(')')}
        fuzzy_matches = {k: v for k, v in details.items() if k.endswith(')')}

        # Main score from unique keywords (1 point per exact, similarity score per fuzzy)
        score = (len(exact_matches) * 1.0) + sum(fuzzy_matches.values())
        
        # Add a small tie-breaker bonus based on the frequency of exact matches
        frequency_bonus = sum(exact_matches.values()) * FREQUENCY_BONUS_WEIGHT
        result['score'] = score + frequency_bonus
        
        result['matched_keywords_count'] = len(details)
        result['matched_keywords_details'] = dict(details)

    final_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_results = final_results[:top_n]

    total_processing_time = time.perf_counter() - total_timer_start
    timing_info = {
        'exact_match_time': round(exact_match_duration, 4),
        'fuzzy_match_time': round(fuzzy_match_duration, 4),
        'total_processing_time': round(total_processing_time, 4),
        "cvs_processed": len(cv_data_for_processing),
        'status_message': f"Search complete. Found {len(final_results)} potential matches."
    }

    return top_results, timing_info

def get_cv_summary_details(cv_path: str) -> dict | None:
    # Extracts detailed structured information for the summary page.
    full_path = get_cv_path(cv_path)
    if not full_path:
        return None
    
    raw_text, _ = extract_text_from_pdf(full_path)
    if raw_text is None:
        return None
        
    return extract_all_cv_details(raw_text)