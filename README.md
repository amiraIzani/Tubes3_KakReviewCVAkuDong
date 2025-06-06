# Tubes3_KakReviewCVAkuDong

## Project Overview

This project is a desktop-based Applicant Tracking System (ATS) built for the IF2211 Algorithm Strategy course. The application parses candidate CVs from PDF files and allows a user (such as a recruiter) to search for relevant candidates using keywords. The system then ranks the CVs based on keyword matches found using specific pattern matching algorithms.

- **Boyer-Moore (BM)**
- **Knuth-Morris-Pratt (KMP)**
- **Levenshtein Distance**

## Prereq
- Python ≥ 3.10
- MySQL Server (Community Edition is recommended)
- Git for cloning the repository


# App Installation & Usage

## Local Installation

Follow these steps to set up and run the application on your local machine.

1.  **Clone this repository:**
    ```shell
    git clone [URL_to_this_repository]
    ```

2.  **Navigate to the project directory:**
    ```shell
    cd src
    ```

3.  **Create and activate a Python virtual environment:**
    ```shell
    # Create the virtual environment
    python -m venv .venv

    # Activate the environment
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

4.  **Install the required Python packages:**
    ```shell
    pip install -r requirements.txt
    ```

5.  **Configure your local database connection:**
    ```shell
    # First, copy the example environment file
    cp .env.example .env
    ```
    Next, open the newly created `.env` file in a text editor and **enter your local MySQL password** for the `ATS_DB_PASS` variable.

6.  **Perform the one-time database setup:**
    - Open a MySQL client (like MySQL Workbench) and run this command to create the database:
        ```sql
        CREATE DATABASE IF NOT EXISTS ats_db;
        ```
7. 
    In the src/ directory, run the main script to create the tables, seed the initial data in the terminal, and rank the CVs from data/:
    ```bash
    python main.py
    ```
8.  Your setup is now complete!

</br>

## Team Information

| Name | ID | Class |
| :--- | :--- | :--- |
| Samantha Laqueenna Ginting | `13523138` | K3 |
| Amira Izani | `13523143` | K3 |
| Asybel B.P. Sianipar | `15223011` | K1 |
