import flet as ft
import json
from core.search_engine import perform_search
from gui.hasilPencarian import ResultPage

def PencarianPage(page: ft.Page):
    FIELD_WIDTH = 550

    keywords_to_search = ft.TextField(
        label="Contoh: python, react, sql",
        width=FIELD_WIDTH,
        border_color="#36618E"
    )
    top_n_results = ft.TextField(
        label="Contoh: 12",
        width=FIELD_WIDTH,
        input_filter=ft.NumbersOnlyInputFilter(),
        border_color="#36618E"
    )
    algorithm_choice = ft.Dropdown(
        label="Pilih Algoritma",
        width=FIELD_WIDTH,
        border_color="#36618E",
        options=[
            ft.dropdown.Option("KMP"),
            ft.dropdown.Option("BM"),
            ft.dropdown.Option("AC"),
        ]
    )

    # Ref untuk teks status di bawah tombol
    search_status_text = ft.Ref[ft.Text]()

    # Event handler
    def handle_search(e):
        search_status_text.current.value = "Kami sedang searching nih kak... Ditunggu sebentar ya!"
        search_status_text.current.color = "#36618E"
        page.update()
        
        keyword = keywords_to_search.value.strip()
        jumlah = top_n_results.value.strip()
        algo = algorithm_choice.value

        if not keyword or not jumlah or not jumlah.isdigit() or not algo:
            search_status_text.current.value = "Waduh, mohon lengkapi semua field pencarian dulu ya kak!"
            search_status_text.current.color = "red"
            page.update()
            return

        jumlah_int = int(jumlah)

        print(f"[PENCARIAN] Keyword: {keyword}, Jumlah: {jumlah_int}, Algoritma: {algo}")

        top_results, timing_info = perform_search(
            keywords_str=keyword,
            algorithm_choice=algo,
            top_n=jumlah_int
        )

        page.session.set("search_results", top_results)
        page.session.set("search_timings", timing_info)
        
        page.session.set("search_params", {
            "keywords": keyword,
            "top_n": jumlah_int,
            "algorithm": algo
        })

        search_status_text.current.value = ""
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
                                    ft.TextButton("Beranda", style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, decoration=ft.TextDecoration.UNDERLINE)), on_click=lambda _: page.go("/")),
                                    ft.TextButton("Pencarian", style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, decoration=ft.TextDecoration.UNDERLINE)), on_click=lambda _: page.go("/pencarian")),
                                    ft.TextButton("Tentang Kru", style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, decoration=ft.TextDecoration.UNDERLINE)), on_click=lambda _: page.go("/tentang"))
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
                                    ft.Text("Yuk Cari Kandidat Terbaik, Kak! 👤", size=48, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                    ft.Text("Masukkan beberapa informasi berikut untuk mencari kandidat.", size=18, text_align=ft.TextAlign.CENTER),

                                    ft.Column(
                                        spacing=10,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Container(
                                                width=FIELD_WIDTH,
                                                content=ft.Text("Kata Kunci*", size=16, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.LEFT)
                                            ),
                                            keywords_to_search,
                                            ft.Container(
                                                width=FIELD_WIDTH,
                                                content=ft.Text("Jumlah Hasil*", size=16, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.LEFT)
                                            ),
                                            top_n_results,
                                            ft.Container(
                                                width=FIELD_WIDTH,
                                                content=ft.Text("Algoritma Pencarian*", size=16, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.LEFT)
                                            ),
                                            algorithm_choice,

                                            ft.Container(height=15),
                                            ft.TextButton(
                                                on_click=handle_search,
                                                style=ft.ButtonStyle(
                                                    bgcolor="#E8EDF6",
                                                    padding=ft.padding.symmetric(horizontal=50, vertical=20),
                                                    shape=ft.RoundedRectangleBorder(radius=50),
                                                    elevation=3,
                                                    side=ft.BorderSide(1, "#36618E"),
                                                ),
                                                content=ft.Text(
                                                    "Cari Sekarang!",
                                                    size=18,
                                                    color="#36618E"
                                                )
                                            ),
                                            ft.Text(value="", ref=search_status_text, size=14)
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