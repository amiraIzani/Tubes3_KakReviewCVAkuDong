import flet as ft
import os
from utils.file_handler import open_file_with_default_app
from core.regex import extract_all_cv_details
from core.pdf_to_text import extract_text_from_pdf

def ResultPage(results: list[dict], timings: dict, page: ft.Page):
    text_color = "white" if page.theme_mode == "dark" else "black"

    # Komponen card CV
    def build_cv_card(match: dict):
        def on_summary_click():
            try:
                cv_path = match.get("cv_path", "")
                full_path = os.path.join("data", cv_path)
                
                print(f"Current CV path: {cv_path}")
                print(f"Full path: {full_path}")
                
                text = extract_text_from_pdf(full_path)[0] or ""
                
                if not text.strip():
                    print("Warning: Extracted text is empty")
                    return
                
                summary_data = extract_all_cv_details(text)
                print(f"Summary data extracted: {summary_data}")
                
                if page.session.contains_key("summary_data"):
                    page.session.remove("summary_data")
                page.session.set("summary_data", summary_data)
                
                page.go("/summary")
                
            except Exception as e:
                print(f"Error in on_summary_click: {e}")
                import traceback
                traceback.print_exc()

        return ft.Container(
            width=300,
            height=320,
            padding=20,
            margin=5,
            border_radius=20,
            bgcolor="#E8EDF6",
            border=ft.border.all(1, text_color),
            content=ft.Column(
                spacing=10,
                expand=True,
                controls=[
                    ft.Text(match.get("name", "N/A"), size=20, weight=ft.FontWeight.BOLD, color=text_color),
                    ft.Text(f"{match.get('matched_keywords_count', 0)} matches", size=14, color=text_color),
                    ft.Text(
                        "\nMatched keywords:\n" + "\n".join([
                            f"{k}: {v} occurrence{'s' if v > 1 else ''}"
                            for k, v in match.get("matched_keywords_details", {}).items()
                        ]),
                        size=13,
                        color=text_color
                    ),
                    ft.Container(expand=True),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                        controls=[
                            ft.TextButton(
                                on_click=lambda _, match_data=match: on_summary_click(),
                                style=ft.ButtonStyle(
                                bgcolor="#ffffff",
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                shape=ft.RoundedRectangleBorder(radius=30),
                                elevation=2,
                                side=ft.BorderSide(1, "#36618E"),
                                ),
                                content=ft.Text(
                                    "Summary",
                                    size=13,
                                    color="#36618E"
                                )
                            ),
                            ft.TextButton(
                                on_click=lambda _, path=match.get("cv_path", ""): open_file_with_default_app(os.path.join("data", path)),
                                style=ft.ButtonStyle(
                                bgcolor="#ffffff",
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                shape=ft.RoundedRectangleBorder(radius=30),
                                elevation=2,
                                side=ft.BorderSide(1, "#36618E"),
                                ),
                                content=ft.Text(
                                    "Lihat CV",
                                    size=13,
                                    color="#36618E"
                                )
                            ),
                        ]
                    )
                ]
            )
        )

    # Bangun grid: 3 kolom per baris
    rows = []
    row = []
    for i, match in enumerate(results):
        row.append(build_cv_card(match))
        if (i + 1) % 3 == 0 or i == len(results) - 1:
            rows.append(ft.Row(controls=row, alignment=ft.MainAxisAlignment.CENTER, spacing=10))
            row = []

    # Info waktu
    match_info = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
        controls=[
            ft.Text("Hasil Pencarian 🔍", size=45, weight=ft.FontWeight.BOLD),
            ft.Text(f"{len(results)} CV ditemukan!", size=18, color="#36618E", weight=ft.FontWeight.W_600),
            ft.Text(
                f"Exact Match: {timings.get('cvs_processed', 0)} CVs di-scan dalam {timings.get('exact_match_time', '0')}s.\n"
                f"Fuzzy Match: {timings.get('cvs_processed', 0)} CVs di-scan dalam {timings.get('fuzzy_match_time', '0')}s.",
                size=18,
                text_align=ft.TextAlign.CENTER
            )
        ]
    )

    # Navigation bar
    navbar = ft.Container(
        padding=ft.padding.symmetric(vertical=40),
        alignment=ft.alignment.top_center,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=200,
            controls=[
                ft.TextButton("Beranda", style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, decoration=ft.TextDecoration.UNDERLINE)), on_click=lambda _: page.go("/")),
                ft.TextButton("Pencarian", style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, decoration=ft.TextDecoration.UNDERLINE)), on_click=lambda _: page.go("/pencarian")),
                ft.TextButton("Tentang Kru", style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, decoration=ft.TextDecoration.UNDERLINE)), on_click=lambda _: page.go("/tentang"))
            ]
        )
    )

    # Final View
    return ft.View(
        route="/hasil",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.padding.all(40),
                alignment=ft.alignment.top_center,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        navbar,
                        match_info,
                        *rows
                    ]
                )
            )
        ]
    )