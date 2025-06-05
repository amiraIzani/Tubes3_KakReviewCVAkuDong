import os
from datetime import date
from faker import Faker

from model.models import (
    insert_applicant_profile,
    insert_application_detail,
)

from model.database import fetch_one

fake = Faker()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(THIS_DIR, '..', '..', 'data'))

def _split_name(full_name: str) -> tuple[str | None, str | None]:
    # Helper to split a full name into first and last names.
    parts = full_name.split()
    if not parts:
        return None, None
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else None
    return first_name, last_name

def seed_with_dummy_data():
    if not os.path.isdir(DATA_DIR):
        print(f"[SeedDummy] Data folder is not found: {DATA_DIR}")
        return

    print(f"[SeedDummy] Looking for PDF files in: {DATA_DIR}")
    file_count = 0
    processed_files = 0

    for filename in os.listdir(DATA_DIR):
        if not filename.lower().endswith('.pdf'):
            continue

        processed_files +=1
        identifier = filename[:-4] # Use filename without .pdf as a unique id
        full_pdf_path = os.path.join(DATA_DIR, filename)
        print(f"\n[SeedDummy] Processing file: {filename}  -> identifier='{identifier}'")

        applicant_id = None
        existing_applicant_data = None

        try:
            # Check if an applicant with this identifier already exists
            existing_applicant_data = fetch_one(
                "SELECT applicant_id FROM ApplicantProfile WHERE identifier = %s",
                (identifier,)
            )
        except Exception as e:
            print(f"  [ERROR] Failed to check ApplicantProfile for identifier '{identifier}': {e}")
            continue

        if existing_applicant_data:
            applicant_id = existing_applicant_data[0] # The first column is applicant_id
            print(f"  [Info] Identifier '{identifier}' already exists with applicant_id={applicant_id}.")
        else:
            # Generate fake data for a new applicant
            full_name = fake.name()
            first_name, last_name = _split_name(full_name)
            email = fake.email()
            phone_number = fake.phone_number()
            address = fake.address().replace('\n', ', ')
            date_of_birth_val = fake.date_of_birth(minimum_age=22, maximum_age=60)

            print(f"  [Info] Creating new ApplicantProfile for identifier '{identifier}':")
            print(f"    Name: {first_name} {last_name}, Email: {email}")

            try:
                applicant_id = insert_applicant_profile(
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth_val,
                    address=address,
                    phone_number=phone_number,
                    email=email,
                    identifier=identifier
                )
                if applicant_id is None:
                    print(f"  [ERROR] Failed to insert ApplicantProfile for identifier '{identifier}', received None ID.")
                    continue
                print(f"  [Insert] New ApplicantProfile created: applicant_id={applicant_id}")
            except Exception as e:
                print(f"  [ERROR] Failed to insert ApplicantProfile for identifier '{identifier}': {e}")
                continue

        # Proceed to insert ApplicationDetail, whether applicant was existing or newly created
        if applicant_id is not None:
            try:
                # Setting application_role to a fake job title or None for dummy data
                application_role_val = fake.job() if fake.boolean(chance_of_getting_true=75) else None

                print(f"  [Info] Creating new ApplicationDetail for applicant_id={applicant_id}")
                detail_id = insert_application_detail(
                    applicant_id=applicant_id,
                    cv_path=full_pdf_path,
                    application_role=application_role_val, # Changed from position
                    applied_date=date.today() # Defaulting to today
                )
                if detail_id is None:
                     print(f"  [ERROR] Failed to insert ApplicationDetail for applicant_id {applicant_id}, received None ID.")
                     continue
                print(f"  [Insert] New ApplicationDetail created: detail_id={detail_id}, cv_path='{full_pdf_path}'")
                file_count += 1
            except Exception as e:
                print(f"  [ERROR] Failed to insert ApplicationDetail for applicant_id {applicant_id}: {e}")
                continue # Skip to the next file
        else:
            print(f"  [Warning] Skipping ApplicationDetail for '{filename}' as applicant_id was not determined.")


    if processed_files == 0:
        print(f"[SeedDummy] No PDF files found in {DATA_DIR}.")
    else:
        print(f"\n[SeedDummy] Finished processing. Successfully created ApplicationDetail entries for {file_count} out of {processed_files} PDF files found.")

if __name__ == '__main__':
    print("Starting dummy data seeding process...")
    seed_with_dummy_data()
    print("Dummy data seeding process completed.")