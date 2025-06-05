# MySQL connection logic

import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import os

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
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[Database] Error connecting to MySQL: {e}")
        return None

# CONTEXT MANAGER FOR CURSOR
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
    except Error as e:
        conn.rollback()
        print(f"[database.py][get_db_cursor] Error when executing query: {e}")
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
            cursor.execute(query, params)
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
    conn = get_db_connection()
    if conn is None:
        raise Exception("Cannot connect to the database.")
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        conn.rollback()
        print(f"[database.py][insert_and_get_id] Error: {e}\nQuery: {query}")
        raise
    finally:
        cursor.close()
        conn.close()