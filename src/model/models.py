# ApplicantProfile & ApplicationDetail tables

from .database import execute_query, fetch_all, fetch_one, insert_and_get_id
from datetime import date

# ----------- CREATE TABLE IF NOT EXISTS -----------
def create_tables():
    # create ApplicantProfile & ApplicationDetail tables

    # ApplicantProfile
    sql_profile = """
    CREATE TABLE IF NOT EXISTS ApplicantProfile (
        applicant_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) DEFAULT NULL,
        last_name VARCHAR(50) DEFAULT NULL,
        date_of_birth DATE DEFAULT NULL,
        address VARCHAR(255) DEFAULT NULL,
        phone_number VARCHAR(20) DEFAULT NULL,
        email VARCHAR(255) UNIQUE,                      -- Added for practical use + seeding
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Added for auditing
        identifier VARCHAR(255) UNIQUE                  -- Added for seeding idempotency
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    execute_query(sql_profile)

    # ApplicationDetail
    sql_application = """
    CREATE TABLE IF NOT EXISTS ApplicationDetail (
        detail_id INT AUTO_INCREMENT PRIMARY KEY,
        applicant_id INT NOT NULL,
        application_role VARCHAR(100) DEFAULT NULL,
        cv_path TEXT NOT NULL,                          -- Changed to TEXT as per PDF
        applied_date DATE DEFAULT NULL,                 -- Added for practical use
        FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    execute_query(sql_application)

    print("[models.py][create_tables] ApplicantProfile and ApplicationDetail Tables are successfully created.")

# ----------- INSERT FUNTIONS -----------
def insert_applicant_profile(
        first_name: str = None,
        last_name: str = None,
        date_of_birth: date = None,
        address: str = None,
        phone_number: str = None,
        email: str = None,
        identifier: str = None  # For seeding
    ) -> int | None:
    # insert one record into ApplicantProfile table
    # return: id (AUTO_INCREMENT)

    _first_name = first_name
    _last_name = last_name

    sql = """
        INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number, email, identifier)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    params = (_first_name, _last_name, date_of_birth, address, phone_number, email, identifier)
    try:
        new_id = insert_and_get_id(sql, params)
        return new_id
    except Exception as e:
        print(f"[models.py][insert_applicant_profile] Failed: {e}")
        # Decide whether to return None or re-raise. For now, re-raising.
        raise

def insert_application_detail(
    applicant_id: int,
    cv_path: str,
    application_role: str = None,
    applied_date: date = None
) -> int | None:
    # insert one record into ApplicationDetail table
    # return: id (AUTO_INCREMENT)

    if applied_date is None:
        applied_date = date.today()
    sql = """
        INSERT INTO ApplicationDetail (applicant_id, cv_path, application_role, applied_date)
        VALUES (%s, %s, %s, %s);
    """
    params = (applicant_id, cv_path, application_role, applied_date)
    try:
        new_id = insert_and_get_id(sql, params)
        return new_id
    except Exception as e:
        print(f"[models.py][insert_application_detail] Failed: {e}")
        # Decide whether to return None or re-raise. For now, re-raising.
        raise

# FETCH FUNCTIONS
def fetch_all_cv_details():
    sql = """
        SELECT detail_id, applicant_id, application_role, cv_path, applied_date
        FROM ApplicationDetail;
    """
    try:
        rows = fetch_all(sql) # Assumes fetch_all returns list or raises error
        return rows
    except Exception as e:
        print(f"[models.py][fetch_all_cv_details] Failed: {e}")
        raise

def fetch_applicant_by_id(applicant_id_val: int) -> dict | None:
    sql = """
        SELECT applicant_id, first_name, last_name, date_of_birth, address, phone_number, email, created_at, identifier
        FROM ApplicantProfile
        WHERE applicant_id = %s;
    """
    params = (applicant_id_val,)
    try:
        row = fetch_one(sql, params) # fetch_one returns a tuple or None
        if row:
            return {
                "applicant_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "date_of_birth": row[3],
                "address": row[4],
                "phone_number": row[5],
                "email": row[6],
                "created_at": row[7],
                "identifier": row[8]
            }
        return None
    except Exception as e:
        print(f"[models.py][fetch_applicant_by_id] Failed: {e}")
        # Returning None on error here, as per original logic.
        # Consider if re-raising specific DB errors might be better.
        return None