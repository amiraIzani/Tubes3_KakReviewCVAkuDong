import flet as ft

def TentangPage(page: ft.Page):
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
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
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

                                    # Daftar kru
                                    ft.Column(
                                        spacing=20,
                                        controls=[
                                            ft.Card(
                                                content=ft.Container(
                                                    padding=20,
                                                    content=ft.Column(
                                                        spacing=5,
                                                        controls=[
                                                            ft.Text("Asybel B. P. Sianipar", size=20, weight=ft.FontWeight.BOLD),
                                                            ft.Text("Arsitektur 2023"),
                                                            ft.Text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis convallis, augue vel consectetur ullamcorper.")
                                                        ]
                                                    )
                                                )
                                            ),
                                            ft.Card(
                                                content=ft.Container(
                                                    padding=20,
                                                    content=ft.Column(
                                                        spacing=5,
                                                        controls=[
                                                            ft.Text("Samantha Laqueenna Ginting", size=20, weight=ft.FontWeight.BOLD),
                                                            ft.Text("Teknik Informatika 2023"),
                                                            ft.Text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis convallis, augue vel consectetur ullamcorper.")
                                                        ]
                                                    )
                                                )
                                            ),
                                            ft.Card(
                                                content=ft.Container(
                                                    padding=20,
                                                    content=ft.Column(
                                                        spacing=5,
                                                        controls=[
                                                            ft.Text("Amira Izani", size=20, weight=ft.FontWeight.BOLD),
                                                            ft.Text("Teknik Informatika 2023"),
                                                            ft.Text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis convallis, augue vel consectetur ullamcorper.")
                                                        ]
                                                    )
                                                )
                                            ),
                                        ]
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
