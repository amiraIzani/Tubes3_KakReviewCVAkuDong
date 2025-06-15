import flet as ft
import os
from .gui.home import HomePage
from .gui.pencarian import PencarianPage
from .gui.tentang import TentangPage
from .gui.summary import SummaryPage

from .core.search_engine import perform_search
from .model.models import create_tables
from .utils.data_seeding import seed_with_dummy_data
from dotenv import load_dotenv

def initialize_backend():
    print("[MAIN] Initializing application environment...")
    load_dotenv()
    print("  - Environment variables loaded.")

    print("  - Ensuring database tables exist...")
    create_tables()

    print("  - Seeding database with CVs...")
    seed_with_dummy_data()

    print("[MAIN] Initialization complete.")

def main(page: ft.Page):
    current_dir = os.path.dirname(__file__)
    font_path_regular = os.path.abspath(os.path.join(current_dir, "gui/fonts/OpenSauceOne-Regular.ttf"))

    page.fonts = {
        "OSO-Regular": font_path_regular,
    }

    page.title = "Kak, Review CV Aku Dong!"
    page.theme = ft.Theme(font_family="OSO-Regular")
    page.theme_mode = ft.ThemeMode.LIGHT  # Force light mode
    page.bgcolor = "#F9FBFD"
    page.scroll = "auto"
    page.update()

    def route_change(route):
        print(f"[ROUTING] Route changed to: {route}")
        
        page.views.clear()
        
        if page.route == "/":
            page.views.append(HomePage(page))
        elif page.route == "/pencarian":
            page.views.append(PencarianPage(page))
        elif page.route == "/tentang":
            page.views.append(TentangPage(page))
        elif page.route == "/summary":
            summary_data = page.session.get("summary_data")
            
            if summary_data is None:
                print("[ROUTING] No summary data found, redirecting to pencarian")
                page.go("/pencarian")
                return
            
            page.views.append(SummaryPage(summary_data, page))
        else:
            print(f"[ROUTING] Unknown route: {route}, redirecting to home")
            page.go("/")
            return
            
        page.update()

    def view_pop(view):
        print(f"[ROUTING] View popped: {view}")
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1] if page.views else None
            if top_view:
                page.go(top_view.route)
        else:
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    page.go(page.route if page.route else "/")

if __name__ == "__main__":
    # 1. First, run the backend setup and data seeding.
    initialize_backend()
    
    # 2. After setup is complete, launch the Flet GUI application.
    print("[MAIN] Launching GUI application...")
    ft.app(target=main)