import os
import mysql.connector

# Load environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "elimu")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Ooliskiawapi@1")
MYSQL_DB = os.getenv("MYSQL_DB", "elimu_db")

def get_mysql_connection():
    """Establish connection to MySQL."""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        if conn.is_connected():
            print("✅ Connected to MySQL successfully")
            return conn
    except mysql.connector.Error as e:
        print(f"❌ MySQL Connection Error: {e}")
        return None

# Test connection when running this file
if __name__ == "__main__":
    conn = get_mysql_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📂 Available tables: {[table[0] for table in tables]}")
        conn.close()
