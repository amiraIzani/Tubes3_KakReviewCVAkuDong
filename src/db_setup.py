import mysql.connector
from mysql.connector import Error
import getpass
import os

# --- Configuration ---
DB_NAME = 'ats_db'
APP_USER = 'ats_user'
APP_PASSWORD = 'very_strong_password_123'

def db_setup():
    try:
        root_user = input("Enter your MySQL root username (press Enter for 'root'): ") or 'root'
        root_password = getpass.getpass(f"Enter the MySQL password for user '{root_user}': ")

        print("\nConnecting to MySQL server as root...")
        conn = mysql.connector.connect(
            host='localhost',
            user=root_user,
            password=root_password
        )
        cursor = conn.cursor()
        print("\033[92mSuccessfully connected to MySQL server.\033[0m")

        print(f"\nCreating database '{DB_NAME}' if it does not exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"  - Database '{DB_NAME}' is ready.")

        print(f"Creating application user '{APP_USER}'...")
        try:
            cursor.execute(f"CREATE USER '{APP_USER}'@'localhost' IDENTIFIED BY '{APP_PASSWORD}';")
            print(f"  - User '{APP_USER}' created.")
        except Error as e:
            if e.errno == 1396:
                print(f"  - User '{APP_USER}' already exists. Skipping creation.")
            else:
                raise
        
        print(f"Granting privileges on '{DB_NAME}' to '{APP_USER}'...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{APP_USER}'@'localhost';")
        cursor.execute("FLUSH PRIVILEGES;")
        print("  - Privileges granted.")

        print("\nCreating .env file with application credentials...")
        env_content = (
            f"# Environment variables for the ATS Application\n"
            f"ATS_DB_HOST=localhost\n"
            f"ATS_DB_USER={APP_USER}\n"
            f"ATS_DB_PASS={APP_PASSWORD}\n"
            f"ATS_DB_NAME={DB_NAME}\n"
        )
        
        project_root = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(project_root, '.env')
        
        with open(env_path, 'w') as f:
            f.write(env_content)
            
        print(f"\033[92mSuccessfully created .env file at: {env_path}\033[0m")

        print("\n\033[92mDatabase setup is complete! You can now run the main application.\033[0m")
        print("Next steps: Run your seeding script (e.g., `python -m src.main`) to create the tables.")

    except Error as e:
        print(f"\n\033[91mAn error occurred: {e}\033[0m")
        print("\033[91mPlease check that your MySQL server is running and that the root credentials are correct.\033[0m")
    
    finally:
        # Ensure the connection is closed
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nConnection to MySQL server closed.")

if __name__ == "__main__":
    db_setup()
