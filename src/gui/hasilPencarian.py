import flet as ft
import os
from utils.file_handler import open_file_with_default_app

def ResultPage(results: list[dict], timings: dict, page: ft.Page):
    # Komponen card CV
    def build_cv_card(match: dict):
        return ft.Container(
            width=300,
            height=320,
            padding=20,
            margin=5,
            border_radius=20,
            bgcolor="#F2F3FB",
            border=ft.border.all(1, "black"),
            content=ft.Column(
                spacing=10,
                expand=True,
                controls=[
                    ft.Text(match.get("name", "N/A"), size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{match.get('matched_keywords_count', 0)} matches", size=14),
                    ft.Text(
                        "\nMatched keywords:\n" + "\n".join([
                            f"{k}: {v} occurrence{'s' if v > 1 else ''}"
                            for k, v in match.get("matched_keywords_details", {}).items()
                        ]),
                        size=13
                    ),
                    ft.Container(
                        expand=True
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                        controls=[
                            ft.ElevatedButton(
                                text="Summary",
                                on_click=lambda _: print(f"Summary for {match['name']}"),
                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=30),
                                                    elevation=2,
                                                    padding=ft.padding.symmetric(horizontal=10, vertical=10)
                                                ),
                            ),
                            ft.ElevatedButton(
                                text="Lihat CV",
                                on_click=lambda _: open_file_with_default_app(os.path.join("data", match.get("cv_path", ""))),
                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=30),
                                                    elevation=2,
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                                ),
                            )
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
            rows.append(ft.Row(controls=row, alignment=ft.MainAxisAlignment.CENTER, spacing=10))  # spacing antar kolom lebih kecil
            row = []


    # Info waktu
    match_info = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
        controls=[
            ft.Text("Hasil Pencarian 🔍", size=45, weight=ft.FontWeight.BOLD),
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
                ft.TextButton("Homepage", style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, decoration=ft.TextDecoration.UNDERLINE)), on_click=lambda _: page.go("/")),
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
