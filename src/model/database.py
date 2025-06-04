# MySQL connection logic

import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='username',
            password='password',
            database='ats_db',
            charset='utf8mb4'
        )
        return conn
    except Error as e:
        print(f"[Database] Error connecting to MySQL: {e}")
        return None
    
def execute_query(query: str, params: tuple = None):
    conn = get_db_connection()
    if conn is None:
        raise Exception("Cannot connect to the database.")
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        cursor.commit()
    except Error as e:
        print(f"[Database] Error executing query: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def fetch_all(query: str, params: tuple = None):
    conn = get_db_connection()
    if conn is None:
        raise Exception("Cannot connect to the database.")
    try:
        cursor = conn.cursor(dictionary=False)
        # Use dictionary=True if we want results as dictionaries
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"[Database] Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        conn.close()