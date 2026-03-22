import csv
import os
from database.db_connection import get_db_connection, init_db

def load_csv_data(csv_file_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM internships")
    if cursor.fetchone()[0] > 0:
        print("Data already loaded into internships table.")
        conn.close()
        return

    print("Loading data from CSV...")
    with open(csv_file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO internships (company_name, location, stipend, skills_required, hiring_status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (row['Name'], row['location'], row['stipend'], row['skills'], row['hiring'])
            )
            
    conn.commit()
    conn.close()
    print("Data successfully loaded into internships table.")

if __name__ == '__main__':
    init_db()
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "WebScraping_Data.csv")
    load_csv_data(csv_path)
