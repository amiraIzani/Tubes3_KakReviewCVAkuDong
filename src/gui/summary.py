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

    def handle_back():
        if page.session.contains_key("summary_data"):
            page.session.remove("summary_data")
        
        search_results = page.session.get("search_results")
        search_timings = page.session.get("search_timings")
        
        if search_results is not None and search_timings is not None:
            from ..gui.hasilPencarian import ResultPage
            page.views.append(ResultPage(search_results, search_timings, page))
            page.update()
        else:
            page.go("/pencarian")

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

    # Tombol back
    back_button = ft.Container(
        alignment=ft.alignment.center_left,
        content=ft.TextButton(
            on_click=lambda _: handle_back(),
            style=ft.ButtonStyle(
                bgcolor="#ffffff",
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                shape=ft.RoundedRectangleBorder(radius=30),
                elevation=2,
                side=ft.BorderSide(1, "#36618E"),
            ),
            content=ft.Row(
                spacing=5,
                tight=True,
                controls=[
                    ft.Text("Kembali", size=20, color="#36618E")
                ]
            )
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
                    spacing=15,
                    controls=[
                        navbar,
                        ft.Container(
                            width=1000,
                            padding=ft.padding.symmetric(horizontal=20),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                spacing=1,
                                controls=[
                                    ft.Text("Ringkasan CV 📝", size=40, weight=ft.FontWeight.BOLD),
                                    back_button
                                ]
                            )
                        ),
                        center_card
                    ]
                )
            )
        ]
    )