import json
from dotenv import load_dotenv

load_dotenv()

from core.search_engine import perform_search
from model.models import create_tables
from utils.data_seeding import seed_with_dummy_data

def pretty_print_results(results: list[dict], timings: dict[str, any]):
    # Formats the search results for clear console output. This helps visualize the data contract for the GUI team.

    print("\n" + "="*60)
    print("        BACKEND TEST RUN COMPLETE - ATS SEARCH RESULTS")
    print("="*60 + "\n")

    print("--- Search Timings & Stats ---")
    print(f"  {'Total CVs Processed':<25}: {timings.get('cvs_processed', 'N/A')}")
    print(f"  {'Exact Match Time (s)':<25}: {timings.get('exact_match_time', 'N/A')}")
    print(f"  {'Fuzzy Match Time (s)':<25}: {timings.get('fuzzy_match_time', 'N/A')}")
    print(f"  {'Total Processing Time (s)':<25}: {timings.get('total_processing_time', 'N/A')}")
    print(f"  {'Status':<25}: {timings.get('status_message', 'N/A')}")
    
    print("\n--- Top Matching CVs ---")
    if not results:
        print("No relevant CVs found for the given keywords.")
    else:
        for i, match in enumerate(results, 1):
            # The score is rounded for cleaner display
            score = round(match.get('score', 0.0), 2)
            print(f"\n--- Rank #{i} | Score: {score} ---")
            print(f"  Name         : {match.get('name', 'N/A')}")
            print(f"  Applicant ID : {match.get('applicant_id', 'N/A')}")
            print(f"  CV Path      : {match.get('cv_path', 'N/A')}")
            print(f"  Matched Words: {match.get('matched_keywords_count', 'N/A')}")
            # Using json.dumps for a nicely formatted dictionary print
            details = match.get('matched_keywords_details', {})
            print(f"  Match Details: {json.dumps(details, indent=4)}")

    print("\n" + "="*60)

if __name__ == "__main__":
    # This block now serves as an INTERACTIVE test harness for the backend.
    
    # --- 1. SETUP PHASE ---
    # This phase ensures the database and its data are ready for searching.
    print("[MAIN] Initializing application environment...")
    print("  - Creating database tables if they don't exist...")
    create_tables()
    
    print("  - Seeding database with CVs from /data directory (will not create duplicates)...")
    seed_with_dummy_data()
    print("[MAIN] Database setup and seeding complete.")
    
    # --- 2. GET USER INPUT ---
    # This section replaces the hardcoded test parameters.
    print("\n" + "-"*60)
    print("               ATS Backend Interactive Test")
    print("-"*60)
    
    keywords_to_search = input("Enter keywords, separated by commas (e.g., python, sql): ")

    # Loop to get a valid algorithm choice
    while True:
        algo_choice_input = input("Choose an algorithm (KMP, BM, or AC for Aho-Corasick): ").upper()
        if algo_choice_input in ["KMP", "BM", "AC"]:
            algorithm_choice = algo_choice_input
            break
        else:
            print("Invalid choice. Please enter KMP, BM, or AC.")
            
    # Loop to get a valid number for top results
    while True:
        try:
            top_n_input = input("How many top results to display? (e.g., 5): ")
            top_n_results = int(top_n_input)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("\n" + "-"*60)
    print(f"[MAIN] Starting backend search...")
    print(f"[MAIN] Keywords: '{keywords_to_search}'")
    print(f"[MAIN] Algorithm: {algorithm_choice}")
    print(f"[MAIN] Top N: {top_n_results}")
    print("-"*60)
    
    # --- 3. EXECUTE THE SEARCH ---
    # This single function call runs the entire backend pipeline with the user's inputs.
    top_results, timing_info = perform_search(
        keywords_str=keywords_to_search,
        algorithm_choice=algorithm_choice,
        top_n=top_n_results
    )
    
    # --- 4. DISPLAY THE RESULTS ---
    # The output shows exactly what the backend provides to the frontend.
    pretty_print_results(top_results, timing_info)