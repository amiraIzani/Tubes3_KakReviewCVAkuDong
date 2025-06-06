# Logic to rank CVs

import time
import os
from collections import defaultdict

from core.pdf_to_text import extract_text_from_pdf
from core.string_matcher import kmp_search, boyer_moore_search, levenshtein_distance
from core.regex import extract_all_cv_details

from model.models import fetch_applicant_by_id
from model.models import fetch_all_cv_details as fetch_all_cv_application_details


DEFAULT_LEVENSTHEIN_SIMILARITY_THRESHOLD = 0.8

def parse_keywords(keywords_str: str) -> list[str]:
    if not keywords_str:
        return []
    return [kw.strip().lower() for kw in keywords_str.split(",") if kw.strip()]

def calculate_levensthein_similarity(s1: str, s2: str) -> float:
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    
    distance = levenshtein_distance(s1, s2)
    return 1.0 - (distance / max_len)

def perform_search(
        keywords_str: str,
        algorithm_choice: str,  # "KMP" or "BM"
        top_n: int,
        levenshtein_similarity_threshold: float = DEFAULT_LEVENSTHEIN_SIMILARITY_THRESHOLD
) -> tuple[list[dict], dict[str, float | str]]:
    start_total_time = time.perf_counter()

    if algorithm_choice == "KMP":
        search_fn = kmp_search
    elif algorithm_choice == "BM":
        search_fn = boyer_moore_search
    else:
        raise ValueError(f"Invalid algorithm choice: {algorithm_choice}. Must be 'KMP' or 'BM'.")
    
    input_keywords = parse_keywords(keywords_str)
    if not input_keywords:
        end_total_time = time.perf_counter()
        return [], {
            'exact_match_time': 0,
            'fuzzy_match_time': 0,
            'total_processing_time': end_total_time - start_total_time,
            "cvs_processed": 0,
            "status_message": "No keywords provided."
        }
    
    # Fetch all CV data
    all_cv_applications = fetch_all_cv_application_details()
    if not all_cv_applications:
        end_total_time = time.perf_counter()
        return [], {
            'exact_match_time': 0,
            'fuzzy_match_time': 0,
            'total_processing_time': end_total_time - start_total_time,
            "cvs_processed": 0,
            "status_message": "No CVs found in the database."
        }
    
    cv_data_for_processing = []
    applicant_cache = {}
    for app_detail_row in all_cv_applications:
        applicant_id = app_detail_row[1]
        cv_path = app_detail_row[3]

        if applicant_id not in applicant_cache:
            profile = fetch_applicant_by_id(applicant_id)
            if profile:
                first_name = profile.get("first_name", "")
                last_name = profile.get("last_name", "")
                name = f"{first_name} {last_name}".strip() if first_name or last_name else "Unnamed Applicant"
            else:
                name = "Unnamed Applicant"
            applicant_cache[applicant_id] = name
        else:
            name = applicant_cache[applicant_id]
        
        cv_data_for_processing.append({
            'applicant_id': applicant_id,
            'detail_id': app_detail_row[0],
            'name': name,
            'cv_path': cv_path,
        })

    # Pre‐extract all CV texts once
    cv_texts_raw = {}
    for cv_info in cv_data_for_processing:
        raw_text, pm_text = extract_text_from_pdf(cv_info['cv_path'])
        # raw_text for regex, pm_text for pattern matching
        cv_texts_raw[cv_info['applicant_id']] = {
            'raw': raw_text or "",
            'pm': pm_text or ""
        }

    results = []
    cvs_processed_count = 0

    # ----- EXACT MATCHING -----

    start_exact_time = time.perf_counter()
    cv_unmatched_keywords = {}

    for cv_info in cv_data_for_processing:
        cvs_processed_count += 1
        applicant_id = cv_info['applicant_id']
        cv_pm_text = cv_texts_raw[applicant_id]['pm']

        if not cv_pm_text:
            cv_unmatched_keywords[applicant_id] = set(input_keywords)
            continue

        matched_details = defaultdict(int)
        matched_unique = set()

        for keyword in input_keywords:
            occurrences = search_fn(cv_pm_text, keyword)
            if occurrences:
                matched_details[keyword] += len(occurrences)
                matched_unique.add(keyword)
        
        if matched_unique:
            unmatched = set(input_keywords) - matched_unique
            results.append({
                'applicant_id': applicant_id,
                'detail_id': cv_info['detail_id'],
                'name': cv_info['name'],
                'cv_path': cv_info['cv_path'],
                'matched_keywords_count': len(matched_unique),
                'matched_keywords_details': dict(matched_details),
                'score': len(matched_unique)
            })
            cv_unmatched_keywords[applicant_id] = unmatched
        else:
            cv_unmatched_keywords[applicant_id] = set(input_keywords)

    end_exact_time = time.perf_counter()
    exact_match_duration = end_exact_time - start_exact_time

    # ----- FUZZY MATCHING -----
    start_fuzzy_time = time.perf_counter()
    fuzzy_match_performed = False

    results_map = {res['applicant_id']: res for res in results}

    for cv_info in cv_data_for_processing:
        applicant_id = cv_info['applicant_id']
        unmatched_keywords = cv_unmatched_keywords.get(applicant_id, set())
        if not unmatched_keywords:
            continue

        cv_words = cv_texts_raw[applicant_id]['pm'].lower().split()
        if not cv_words:
            continue

        fuzzy_added = False
        for keyword in unmatched_keywords:
            max_dist = int((1.0 - levenshtein_similarity_threshold) * len(keyword))
            for word in cv_words:
                if levenshtein_distance(keyword, word) <= max_dist:
                    fuzzy_added = True
                    break
            if not fuzzy_added:
                continue

            fuzzy_match_performed = True
            if applicant_id in results_map:
                entry = results_map[applicant_id]
                fuzzy_key = f"{keyword} (fuzzy)"
                if fuzzy_key not in entry['matched_keywords_details']:
                    entry['matched_keywords_count'] += 1
                    entry['score'] += 0.5
                    entry['matched_keywords_details'][fuzzy_key] = 1
            else:
                new_entry = {
                    'applicant_id': applicant_id,
                    'detail_id': cv_info['detail_id'],
                    'name': cv_info['name'],
                    'cv_path': cv_info['cv_path'],
                    'matched_keywords_count': 1,
                    'matched_keywords_details': {f"{keyword} (fuzzy)": 1},
                    'score': 0.5
                }
                results.append(new_entry)
                results_map[applicant_id] = new_entry


    end_fuzzy_time = time.perf_counter()
    fuzzy_match_duration = end_fuzzy_time - start_fuzzy_time if fuzzy_match_performed else 0

    # ----- RANK RESULTS -----
    results.sort(key=lambda x: x['score'], reverse=True)
    top_results = results[:top_n]

    end_total_time = time.perf_counter()

    timing_info = {
        'exact_match_time': exact_match_duration,
        'fuzzy_match_time': fuzzy_match_duration,
        'total_processing_time': end_total_time - start_total_time,
        "cvs_processed": cvs_processed_count,
        'status_message': f"Search complete. Found {len(results)} potential matches." if results else "No relevant CVs found."
    }

    return top_results, timing_info
    

def get_cv_summary_details(cv_path: str) -> dict | None:
    raw_text, _ = extract_text_from_pdf(cv_path)
    if raw_text is None:
        return None
    return extract_all_cv_details(raw_text)