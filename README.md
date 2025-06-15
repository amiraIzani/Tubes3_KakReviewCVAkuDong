# ATS-CV-Analyzer (Tubes3_KakReviewCVAkuDong)

## Project Overview

Proyek ini adalah sistem **Applicant Tracking System (ATS)** berbasis desktop yang dibuat untuk mata kuliah IF2211 Strategi Algoritma. Aplikasi ini memproses CV kandidat dari file PDF dan memungkinkan pengguna untuk mencari kandidat yang relevan menggunakan kata kunci. Sistem kemudian memberi peringkat CV berdasarkan kecocokan kata kunci yang ditemukan menggunakan algoritma pencocokan pola tertentu, termasuk metode enkripsi yang aman untuk data pelamar.

* **Exact Matching:** Mengimplementasikan **Knuth-Morris-Pratt (KMP)**, **Boyer-Moore (BM)**, dan **Aho-Corasick (AC)** untuk pencarian kata kunci yang efisien.
* **Pencocokan Fuzzy:** Menggunakan **Levenshtein Distance** untuk menemukan dan memberi peringkat kecocokan dekat untuk kata kunci yang salah eja.
* **Keamanan:** Menggunakan **Vigenère Cipher** yang dibuat khusus untuk mengenkripsi dan melindungi data sensitif pelamar dalam basis data.

## BE & FE

`backend`: Python (with `PyMuPDF`, `mysql-connector-python`)
`frontend`: Flet (A Python GUI Framework)

## Prereq

* Python ≥ 3.10
* MySQL Server (Community Edition is recommended)
* Git for cloning the repository

# App Installation & Usage

## Local Installation

Follow these steps to set up and run the application on your local machine. **All commands should be run from the project's root directory.**

1.  **Clone this repository:**
    ```shell
    git clone [URL_to_your_repository]
    cd Tubes3_KakReviewCVAkuDong
    ```

2.  **Create and activate a Python virtual environment:**
    ```shell
    # Create the virtual environment in the root directory
    python -m venv .venv

    # Activate the environment
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```shell
    pip install -r requirements.txt
    ```

4.  **Perform the One-Time Database Setup:**
    This script will create the database, a secure user for the app, and the `.env` file.
    ```shell
    # Run the setup script as a module from the root
    python -m src.model.db_setup
    ```
    You will be prompted to enter your MySQL root password.

5.  Your setup is now complete!

## Running the Application

To start the application, run the `main.py` script from the project root directory. This will automatically create the necessary tables and seed the data on the first run.
```shell
python -m src.main
```

<br>

# Team Information

| Name | ID | Class |
| :--- | :--- | :--- |
| Samantha Laqueenna Ginting | `13523138` | K3 |
| Amira Izani | `13523143` | K3 |
| Asybel B.P. Sianipar | `15223011` | K1 |