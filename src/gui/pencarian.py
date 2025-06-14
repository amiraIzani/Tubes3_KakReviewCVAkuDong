import flet as ft
import json
from core.search_engine import perform_search
from gui.hasilPencarian import ResultPage

def PencarianPage(page: ft.Page):
    FIELD_WIDTH = 500  # Lebar field seragam untuk semua input

    # Komponen input
    keywords_to_search = ft.TextField(label="Kata Kunci", width=FIELD_WIDTH)
    top_n_results = ft.TextField(label="Jumlah Hasil", width=FIELD_WIDTH, input_filter=ft.NumbersOnlyInputFilter())
    algorithm_choice = ft.Dropdown(
        label="Pilih Algoritma",
        width=FIELD_WIDTH,
        options=[
            ft.dropdown.Option("KMP"),
            ft.dropdown.Option("BM")
        ]
    )

    # Event handler button pencarian
    def handle_search(e):
        keyword = keywords_to_search.value.strip()
        jumlah = top_n_results.value.strip()
        algo = algorithm_choice.value

        # Validasi (STILL NOT WORK...🥹)
        if not keyword or not jumlah or not jumlah.isdigit() or not algo:
            page.snack_bar = ft.SnackBar(content=ft.Text("Mohon lengkapi semua field pencarian."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        jumlah_int = int(jumlah)

        print(f"[PENCARIAN] Keyword: {keyword}, Jumlah: {jumlah_int}, Algoritma: {algo}")

        # Panggil perform_search() dari search_engine.py
        top_results, timing_info = perform_search(
            keywords_str=keyword,
            algorithm_choice=algo,
            top_n=jumlah_int
        )

        page.views.append(ResultPage(top_results, timing_info, page))
        page.update()

    return ft.View(
        route="/pencarian",
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

                        ft.Container(expand=1),

                        # Konten utama pencarian
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                tight=True,
                                spacing=30,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        "Yuk Cari Kandidat Terbaik, Kak! 👤",
                                        size=48,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.Text(
                                        "Masukkan beberapa informasi berikut untuk mencari kandidat.",
                                        size=18,
                                        text_align=ft.TextAlign.CENTER
                                    ),

                                    ft.Column(
                                        spacing=20,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            keywords_to_search,
                                            top_n_results,
                                            algorithm_choice,
                                            ft.ElevatedButton(
                                                bgcolor="000000",
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=30),
                                                    elevation=2,
                                                    padding=ft.padding.symmetric(horizontal=30, vertical=20)
                                                ),
                                                content=ft.Text(
                                                    "Cari Sekarang",
                                                    color="ffffff",
                                                    size=18,
                                                ),
                                                on_click=handle_search
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),

                        ft.Container(expand=1),
                    ]
                )
            )
        ],
        padding=0,
        spacing=0
    )
