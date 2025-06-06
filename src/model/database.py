# MySQL connection logic

import mysql.connector
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# CONNECTION CONFIGURATION
DB_CONFIG = {
    'host': os.getenv('ATS_DB_HOST', 'localhost'),
    'user': os.getenv('ATS_DB_USER', 'root'),
    'password': os.getenv('ATS_DB_PASS', ''),
    'database': os.getenv('ATS_DB_NAME', 'ats_db'),
    'charset': 'utf8mb4',
    'use_unicode': True
}

# CONNECTION FUNCTION
def get_db_connection():
    try:
        conn = mysql.connector.Connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"[Database] Exception connecting to MySQL: {e}")
        return None

# CONTEXT MANAGER FOR CURSOR
@contextmanager
def get_db_cursor(commit: bool = True):
    conn = get_db_connection()
    if conn is None:
        yield None
        return

    cursor = conn.cursor(buffered=True)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[database.py][get_db_cursor] Exception when executing query: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# HELPER FUNCTIONS    
def execute_query(query: str, params: tuple = None):
    with get_db_cursor(commit=True) as cursor:
        if cursor is None:
            raise Exception("Cannot connect to the database.")
        if params:
            cursor.execute(query, params or ())
        else:
            cursor.execute(query)

def fetch_all(query: str, params: tuple = None):
    with get_db_cursor(commit=False) as cursor:
        if cursor is None:
            raise Exception("Cannot connect to the database.")
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        return rows

def fetch_one(query: str, params: tuple = None) -> tuple | None:
    with get_db_cursor(commit=False) as cursor:
        if cursor is None:
            raise ConnectionError("Cannot connect to the database.")
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        row = cursor.fetchone()
        return row

# UTILITY FUNCTION TO INSERT AND GET ID
def insert_and_get_id(query: str, params: tuple = None) -> int:
    with get_db_cursor(commit=True) as cursor:
        if cursor is None:
            raise ConnectionError("Cannot connect to the database to insert data.")
        
        cursor.execute(query, params or ())
        # cursor.lastrowid is available immediately after execute for an INSERT
        return cursor.lastrowid