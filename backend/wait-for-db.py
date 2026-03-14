import time
import psycopg2
import os
import sys

def wait_for_db():
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_name = os.getenv("DB_NAME", "library_db")
    
    max_attempts = 30
    attempt = 0
    
    print(f"Waiting for database {db_host}:{db_port}...")
    
    while attempt < max_attempts:
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                dbname=db_name,
                connect_timeout=1
            )
            conn.close()
            print("Database is ready!")
            return True
        except psycopg2.OperationalError as e:
            attempt += 1
            print(f"Attempt {attempt}/{max_attempts}: Database not ready yet...")
            time.sleep(2)
    
    print("Failed to connect to database after maximum attempts")
    return False

if __name__ == "__main__":
    if not wait_for_db():
        sys.exit(1)
    sys.exit(0)