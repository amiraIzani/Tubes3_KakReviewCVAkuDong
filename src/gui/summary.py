import flet as ft

def SummaryPage(data: dict, page: ft.Page):
    def section(title: str, content: str):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(content if content else "-", size=15, text_align=ft.TextAlign.JUSTIFY)
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

    # Konten card utama
    center_card = ft.Container(
        width=1000,
        padding=30,
        border_radius=20,
        border=ft.border.all(1),
        bgcolor="#E8EDF6",
        content=ft.Column(
            spacing=25,
            controls=[
                section("Summary", data.get("summary", "")),
                section("Skills", data.get("skills", "")),
                section("Education", data.get("education", "")),
                section("Experience", data.get("experience", "")),
            ]
        )
    )

    return ft.View(
        route="/summary",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.padding.symmetric(vertical=40, horizontal=20),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=30,
                    controls=[
                        navbar,
                        ft.Text("Ringkasan CV 📝", size=40, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        center_card
                    ]
                )
            )
        ]
    )
