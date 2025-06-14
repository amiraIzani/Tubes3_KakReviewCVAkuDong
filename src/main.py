# RUN DARI ROOT DIRECTORY SUPAYA BISA IMPORT FONTNYA

import flet as ft
import os
from gui.home import HomePage
from gui.pencarian import PencarianPage
from gui.tentang import TentangPage

def main(page: ft.Page):
    current_dir = os.path.dirname(__file__)
    font_path_regular = os.path.abspath(os.path.join(current_dir, "gui/fonts/OpenSauceOne-Regular.ttf"))

    page.fonts = {
        "OSO-Regular": font_path_regular,
    }

    page.title = "Kak, Review CV Aku Dong!"
    page.theme = ft.Theme(font_family="OSO-Regular")
    page.update()

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(HomePage(page))
        elif page.route == "/pencarian":
            page.views.append(PencarianPage(page))
        elif page.route == "/tentang":
            page.views.append(TentangPage(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)

# import json
# from core.search_engine import perform_search
# from model.models import create_tables
# from utils.data_seeding import seed_with_dummy_data

# # Backend test (Algorithm: booyer moore)

# def pretty_print_results(results: list[dict], timings: dict[str, any]):
#     print("\n" + "="*60)
#     print("        BACKEND TEST RUN COMPLETE - ATS SEARCH RESULTS")
#     print("="*60 + "\n")

#     print("--- Search Timings & Stats ---")
#     print(f"  {'Total CVs Processed':<25}: {timings.get('cvs_processed', 'N/A')}")
#     print(f"  {'Exact Match Time (s)':<25}: {timings.get('exact_match_time', 'N/A')}")
#     print(f"  {'Fuzzy Match Time (s)':<25}: {timings.get('fuzzy_match_time', 'N/A')}")
#     print(f"  {'Total Processing Time (s)':<25}: {timings.get('total_processing_time', 'N/A')}")
#     print(f"  {'Status':<25}: {timings.get('status_message', 'N/A')}")
    
#     print("\n--- Top Matching CVs ---")
#     if not results:
#         print("No relevant CVs found for the given keywords.")
#     else:
#         for i, match in enumerate(results, 1):
#             print(f"\n--- Rank #{i} | Score: {match.get('score', 'N/A')} ---")
#             print(f"  Name         : {match.get('name', 'N/A')}")
#             print(f"  Applicant ID : {match.get('applicant_id', 'N/A')}")
#             print(f"  CV Path      : {match.get('cv_path', 'N/A')}")
#             print(f"  Matched Words: {match.get('matched_keywords_count', 'N/A')}")
#             # Using json.dumps for a nicely formatted dictionary print
#             details = match.get('matched_keywords_details', {})
#             print(f"  Match Details: {json.dumps(details, indent=4)}")

#     print("\n" + "="*60)

# if __name__ == "__main__": 
#     # --- SETUP PHASE ---
#     print("[MAIN] Setting up database tables...")
#     create_tables()
    
#     print("[MAIN] Seeding database with CVs from /data directory...")
#     seed_with_dummy_data()
#     print("[MAIN] Database setup and seeding complete.")
    
#     # --- DEFINE TEST PARAMETERS ---
#     keywords_to_search = "engineering, python, software engineering, hardware, sql"
#     algorithm_choice = "BM"  # Using Boyer-Moore
#     top_n_results = 5
    
#     print("\n" + "-"*60)
#     print(f"[MAIN] Starting backend test...")
#     print(f"[MAIN] Searching for keywords: '{keywords_to_search}'")
#     print(f"[MAIN] Using algorithm: {algorithm_choice}")
#     print(f"[MAIN] Requesting top {top_n_results} results.")
#     print("-"*60)
    
#     # --- EXECUTE THE SEARCH ---
#     top_results, timing_info = perform_search(
#         keywords_str=keywords_to_search,
#         algorithm_choice=algorithm_choice,
#         top_n=top_n_results
#     )
    
#     # --- DISPLAY THE RESULTS ---
#     pretty_print_results(top_results, timing_info)
