# ApplicantProfile & ApplicationDetail tables

from .database import execute_query, fetch_all, fetch_one, insert_and_get_id
from datetime import date

from utils.encryption import encrypt, decrypt

# ----------- CREATE TABLE IF NOT EXISTS -----------
def create_tables():
    # Base64 encoding increases string length, so we change sensitive fields to TEXT
    # to ensure the encrypted strings fit without being truncated.

    sql_profile = """
    CREATE TABLE IF NOT EXISTS ApplicantProfile (
        applicant_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name TEXT DEFAULT NULL,
        last_name TEXT DEFAULT NULL,
        date_of_birth TEXT DEFAULT NULL,
        address TEXT DEFAULT NULL,
        phone_number TEXT DEFAULT NULL,
        email TEXT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        identifier VARCHAR(255) UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    execute_query(sql_profile)

    sql_application = """
    CREATE TABLE IF NOT EXISTS ApplicationDetail (
        detail_id INT AUTO_INCREMENT PRIMARY KEY,
        applicant_id INT NOT NULL,
        application_role VARCHAR(100) DEFAULT NULL,
        cv_path TEXT NOT NULL,
        applied_date DATE DEFAULT NULL,
        FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    execute_query(sql_application)
    print("[models.py] create_tables execution attempted.")

# ----------- INSERT FUNTIONS -----------
def insert_applicant_profile(
        first_name: str = None, last_name: str = None, date_of_birth: date = None,
        address: str = None, phone_number: str = None, email: str = None,
        identifier: str = None
) -> int | None:
    
    # Encrypt all sensitive Personally Identifiable Information (PII) before inserting.
    encrypted_first_name = encrypt(first_name)
    encrypted_last_name = encrypt(last_name)
    encrypted_dob = encrypt(str(date_of_birth)) if date_of_birth else None
    encrypted_address = encrypt(address)
    encrypted_phone = encrypt(phone_number)
    encrypted_email = encrypt(email)

    sql = """
        INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number, email, identifier)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    params = (
        encrypted_first_name, encrypted_last_name, encrypted_dob,
        encrypted_address, encrypted_phone, encrypted_email, identifier
    )
    try:
        new_id = insert_and_get_id(sql, params)
        return new_id
    except Exception as e:
        print(f"[models.py][insert_applicant_profile] Failed: {e}")
        raise

def insert_application_detail(
    applicant_id: int, cv_path: str, application_role: str = None,
    applied_date: date = None
) -> int | None:
    if applied_date is None:
        applied_date = date.today()
    sql = """
        INSERT INTO ApplicationDetail (applicant_id, cv_path, application_role, applied_date)
        VALUES (%s, %s, %s, %s);
    """
    params = (applicant_id, cv_path, application_role, applied_date)
    return insert_and_get_id(sql, params)

# FETCH FUNCTIONS
def fetch_all_cv_details():
    # This function does not need changes.
    sql = "SELECT detail_id, applicant_id, application_role, cv_path, applied_date FROM ApplicationDetail;"
    return fetch_all(sql)

def fetch_applicant_by_id(applicant_id_val: int) -> dict | None:
    sql = """
        SELECT applicant_id, first_name, last_name, date_of_birth, address, phone_number, email, created_at, identifier
        FROM ApplicantProfile
        WHERE applicant_id = %s;
    """
    params = (applicant_id_val,)
    row = fetch_one(sql, params)
    
    if row:
        # Decrypt all sensitive fields after fetching from the database.
        decrypted_dob = None
        decrypted_dob_str = decrypt(row[3])
        if decrypted_dob_str and decrypted_dob_str != 'None':
            try:
                # Convert the decrypted date string back into a date object.
                decrypted_dob = date.fromisoformat(decrypted_dob_str)
            except (ValueError, TypeError):
                decrypted_dob = None # Handle cases where date might be malformed

        return {
            "applicant_id": row[0],
            "first_name": decrypt(row[1]),
            "last_name": decrypt(row[2]),
            "date_of_birth": decrypted_dob,
            "address": decrypt(row[4]),
            "phone_number": decrypt(row[5]),
            "email": decrypt(row[6]),
            "created_at": row[7],
            "identifier": row[8]
        }
    return None