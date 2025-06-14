import os
from dotenv import load_dotenv
from model.database import get_db_connection, execute_query

def reset_database_tables():
    print("[RESET] This script will drop the ApplicantProfile and ApplicationDetail tables.")
    confirm = input("Are you sure you want to continue? This cannot be undone. (y/n): ").lower()
    
    if confirm != 'y':
        print("[RESET] Aborted by user.")
        return
    
    try:
        # We don't need to call a specific execute_query function from database.py,
        # we can just get a connection and run the commands directly.
        print("\n[RESET] Connecting to the database...")
        conn = get_db_connection()
        if not conn:
            raise ConnectionError("Failed to connect to the database. Check your .env settings.")
        
        cursor = conn.cursor()
        print("\033[92m  - Connection successful.\033[0m")

        # Drop tables. ApplicationDetail must be dropped first due to the foreign key constraint.
        print("[RESET] Dropping ApplicationDetail table...")
        cursor.execute("DROP TABLE IF EXISTS ApplicationDetail;")
        print("  - Table 'ApplicationDetail' dropped.")

        print("[RESET] Dropping ApplicantProfile table...")
        cursor.execute("DROP TABLE IF EXISTS ApplicantProfile;")
        print("  - Table 'ApplicantProfile' dropped.")
        
        conn.commit()
        
        print("\n\033[92mDatabase tables have been reset successfully!\033[0m")
        print("You can now run `python -m src.main` to rebuild and re-seed the database.")

    except Exception as e:
        print(f"\n\033[91m[ERROR] An error occurred during reset: {e}\033[0m")
    
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("\n[RESET] Database connection closed.")

if __name__ == "__main__":
    # Load environment variables to connect with the correct user
    load_dotenv()
    reset_database_tables()