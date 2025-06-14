import flet as ft
from utils.file_handler import open_file_with_default_app
import os

def ResultPage(results: list[dict], timings: dict, page: ft.Page):
    # Komponen card CV
    def build_cv_card(match: dict):
        return ft.Container(
            width=300,
            padding=20,
            margin=10,
            border_radius=20,
            bgcolor="000000",
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(match.get("name", "N/A"), size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{match.get('matched_keywords_count', 0)} matches", size=14),
                    ft.Text(
                        "Matched keywords:\n" + "\n".join([
                            f"{k}: {v} occurrence{'s' if v > 1 else ''}"
                            for k, v in match.get("matched_keywords_details", {}).items()
                        ]),
                        size=13
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.ElevatedButton(text="Summary", on_click=lambda _: print(f"Summary for {match['name']}")), # Placeholder untuk fitur summary
                            ft.ElevatedButton(
                                text="Lihat CV",
                                on_click=lambda _: open_file_with_default_app(os.path.join("data", match.get("cv_path", "")))
                            )
                        ]
                    )
                ]
            )
        )

    # Grid per CV
    grid = ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=build_cv_card(match),
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3}
            )
            for match in results
        ]
    )


    # Info waktu
    match_info = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
        controls=[
            ft.Text("Hasil Pencarian", size=32, weight=ft.FontWeight.BOLD),
            ft.Text(
                f"Exact Match: {timings.get('cvs_processed', 0)} CVs di-scan dalam {timings.get('exact_match_time', '0')}s.\n"
                f"Fuzzy Match: {timings.get('cvs_processed', 0)} CVs di-scan dalam {timings.get('fuzzy_match_time', '0')}s.",
                size=14,
                text_align=ft.TextAlign.CENTER
            )
        ]
    )

    return ft.View(
        route="/hasil",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.padding.all(40),
                alignment=ft.alignment.top_center,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=40,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        # Navigation bar
                        ft.Container(
                            padding=ft.padding.symmetric(vertical=40),
                            alignment=ft.alignment.top_center,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=200,  # jarak antar tombol
                                controls=[
                                    ft.TextButton(
                                        "Homepage",
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=20)
                                        ),
                                        on_click=lambda _: page.go("/")
                                    ),
                                    ft.TextButton(
                                        "Pencarian",
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=20)
                                        ),
                                        on_click=lambda _: page.go("/pencarian")
                                    ),
                                    ft.TextButton(
                                        "Tentang Kru",
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=20)
                                        ),
                                        on_click=lambda _: page.go("/tentang")
                                    ),
                                ]
                            )
                        ),
                        match_info,
                        grid
                    ]
                )
            )
        ]
    )
