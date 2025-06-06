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
    
    # Get a list of all PDF files first
    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("[SeedDummy] No PDF files found to process.")
        return

    total_files_processed = 0
    new_applications_created = 0

    for filename in pdf_files:
        total_files_processed += 1
        identifier = filename[:-4]
        full_pdf_path = os.path.join(DATA_DIR, filename)
        
        print(f"\n[SeedDummy] Processing file ({total_files_processed}/{len(pdf_files)}): {filename}")

        # --- Step 1: Get or Create Applicant Profile ---
        applicant_id = None
        try:
            existing_profile = fetch_one(
                "SELECT applicant_id FROM ApplicantProfile WHERE identifier = %s",
                (identifier,)
            )
            if existing_profile:
                applicant_id = existing_profile[0]
                print(f"  [Info] Existing ApplicantProfile found with id={applicant_id}.")
            else:
                # Generate and insert a new applicant profile
                first_name, last_name = _split_name(fake.name()) # Assuming _split_name helper exists
                applicant_id = insert_applicant_profile(
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=fake.date_of_birth(minimum_age=22, maximum_age=60),
                    address=fake.address().replace('\n', ', '),
                    phone_number=fake.phone_number(),
                    email=fake.email(),
                    identifier=identifier
                )
                print(f"  [Insert] New ApplicantProfile created with id={applicant_id}.")
        except Exception as e:
            print(f"  [ERROR] Failed during ApplicantProfile processing: {e}")
            continue # Skip to the next file

        # --- Step 2: Get or Create Application Detail (The Corrected Logic) ---
        if applicant_id is None:
            print(f"  [Warning] Skipping ApplicationDetail for '{filename}' as applicant_id was not determined.")
            continue

        try:
            # check if application already exists
            application_exists = fetch_one(
                "SELECT detail_id FROM ApplicationDetail WHERE applicant_id = %s AND cv_path = %s",
                (applicant_id, full_pdf_path)
            )

            if application_exists:
                print(f"  [Info] ApplicationDetail for this CV already exists (detail_id={application_exists[0]}). Skipping.")
            
            else:
                application_role_val = fake.job() if fake.boolean(chance_of_getting_true=75) else None
                
                print(f"  [Info] Creating new ApplicationDetail for applicant_id={applicant_id}")
                detail_id = insert_application_detail(
                    applicant_id=applicant_id,
                    cv_path=full_pdf_path,
                    application_role=application_role_val,
                    applied_date=date.today()
                )

                if detail_id:
                    print(f"  [Insert] New ApplicationDetail created: detail_id={detail_id}")
                    new_applications_created += 1
                else:
                    print(f"  [ERROR] Failed to insert ApplicationDetail, received None ID.")

        except Exception as e:
            print(f"  [ERROR] Failed to insert ApplicationDetail for applicant_id {applicant_id}: {e}")
            continue

    print(f"\n[SeedDummy] Finished processing. Processed {total_files_processed} PDF files. Created {new_applications_created} new application entries.")

if __name__ == '__main__':
    print("Starting dummy data seeding process...")
    seed_with_dummy_data()
    print("Dummy data seeding process completed.")