import flet as ft

def HomePage(page: ft.Page):
    return ft.View(
        route="/",
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
                                spacing=200, # jarak antar tombol
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
                        
                        # Spacer atas
                        ft.Container(expand=1),

                        # Konten utama
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                tight=True,
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        '"Kak, Review CV Aku Dong! 📑"',
                                        size=64,
                                        weight=ft.FontWeight.BOLD,
                                        color="000000",
                                        text_align=ft.TextAlign.CENTER,
                                        font_family="OSO-Regular"
                                    ),
                                    ft.Container(
                                        margin=ft.margin.symmetric(vertical=30),
                                        content=ft.Text(
                                            "Punten Kak HUHU, maaf banget tapi aku lagi cari staff baru nih...\nIni requirements-nya ya, Kak. Nanti aku izin catch up lagi. HANUPIS!",
                                            size=20,
                                            color="000000",
                                            text_align=ft.TextAlign.CENTER,
                                            font_family="OSO-Regular"
                                        )
                                    ),
                                    ft.ElevatedButton(
                                        on_click=lambda _: page.go("/pencarian"),
                                        bgcolor="000000",
                                        style=ft.ButtonStyle(
                                            padding=ft.padding.symmetric(horizontal=50, vertical=20),
                                            shape=ft.RoundedRectangleBorder(radius=50),
                                            elevation=3,
                                        ),
                                        content=ft.Text(
                                            "Mulai Cari Yuk, Kak!",
                                            color="ffffff",
                                            size=20,
                                        )
                                    )
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
