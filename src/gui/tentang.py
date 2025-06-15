import flet as ft
import webbrowser

def TentangPage(page: ft.Page):
    def open_repo(e):
        webbrowser.open_new_tab("https://github.com/amiraIzani/Tubes3_KakReviewCVAkuDong/")

    return ft.View(
        route="/tentang",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.padding.symmetric(horizontal=40, vertical=20),
                alignment=ft.alignment.center,
                content=ft.Column(
                    expand=True,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        # Navigation bar
                        ft.Container(
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
                        ),

                        # Spacer atas
                        ft.Container(expand=1),

                        # Konten utama
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                tight=True,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=30,
                                controls=[
                                    ft.Text(
                                        "Izin Jump In 🤸‍♀️ Untuk Memperkenalkan Diri Ya Kak!",
                                        size=42,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.Text(
                                        "Ini kami yang ada di balik layar sistem ATS ini. Salam kenal!",
                                        size=18,
                                        text_align=ft.TextAlign.CENTER
                                    ),

                                    # Daftar kru horizontal dengan fixed height + background
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=20,
                                        controls=[
                                            ft.Card(
                                                elevation=2,
                                                content=ft.Container(
                                                    width=300,
                                                    height=220,
                                                    padding=20,
                                                    bgcolor="#E8EDF6",
                                                    border_radius=10,
                                                    border=ft.border.all(1),
                                                    content=ft.Column(
                                                        spacing=5,
                                                        alignment=ft.MainAxisAlignment.START,
                                                        controls=[
                                                            ft.Text("Asybel B. P. Sianipar", size=20, weight=ft.FontWeight.BOLD),
                                                            ft.Text("Arsitektur 2023\n"),
                                                        ]
                                                    )
                                                )
                                            ),
                                            ft.Card(
                                                elevation=2,
                                                content=ft.Container(
                                                    width=300,
                                                    height=220,
                                                    padding=20,
                                                    bgcolor="#E8EDF6",
                                                    border_radius=10,
                                                    border=ft.border.all(1),
                                                    content=ft.Column(
                                                        spacing=5,
                                                        alignment=ft.MainAxisAlignment.START,
                                                        controls=[
                                                            ft.Text("Samantha Laqueenna G.", size=20, weight=ft.FontWeight.BOLD),
                                                            ft.Text("Teknik Informatika 2023\n"),
                                                        ]
                                                    )
                                                )
                                            ),
                                            ft.Card(
                                                elevation=2,
                                                content=ft.Container(
                                                    width=300,
                                                    height=220,
                                                    padding=20,
                                                    bgcolor="#E8EDF6",
                                                    border_radius=10,
                                                    border=ft.border.all(1),
                                                    content=ft.Column(
                                                        spacing=5,
                                                        alignment=ft.MainAxisAlignment.START,
                                                        controls=[
                                                            ft.Text("Amira Izani", size=20, weight=ft.FontWeight.BOLD),
                                                            ft.Text("Teknik Informatika 2023\n"),
                                                        ]
                                                    )
                                                )
                                            ),
                                        ]
                                    ),
                                    ft.TextButton(
                                        on_click=open_repo,
                                        style=ft.ButtonStyle(
                                            bgcolor="#E8EDF6",
                                            padding=ft.padding.symmetric(horizontal=45, vertical=20),
                                            shape=ft.RoundedRectangleBorder(radius=50),
                                            elevation=3,
                                            side=ft.BorderSide(1, "#36618E"),
                                        ),
                                        content=ft.Text(
                                            "Lihat Repositori Kami",
                                            size=18,
                                            color="#36618E"
                                        )
                                    ),
                                ]
                            )
                        ),

                        # Spacer bawah
                        ft.Container(expand=1),
                    ]
                )
            )
        ],
        padding=0,
        spacing=0
    )
