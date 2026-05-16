#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()  # optional, but you can also hardcode credentials for now

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'bank_reviews',
    'user': 'postgres',
    'password': 'Pass@1234'  
}

def main():
    # Load enriched datapython scripts/load_to_db.py
    df = pd.read_csv('data/enriched_reviews.csv')
    print(f"Loaded {len(df)} reviews")

    # Connect
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Get bank_id mapping
    cur.execute("SELECT bank_name, bank_id FROM banks")
    bank_map = {row[0]: row[1] for row in cur.fetchall()}
    print(f"Bank mapping: {bank_map}")

    # Prepare data for insertion
    records = []
    for _, row in df.iterrows():
        bank_id = bank_map.get(row['bank'])
        if bank_id is None:
            print(f"Warning: No bank_id for {row['bank']}")
            continue
        records.append((
            bank_id,
            row['review_text'],
            int(row['rating']),
            row['review_date'],
            row['sentiment_label'],
            float(row['sentiment_score']),
            row['identified_theme'],
            row['source']
        ))

    # Bulk insert
    insert_sql = """
        INSERT INTO reviews 
        (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source)
        VALUES %s
    """
    execute_values(cur, insert_sql, records)
    conn.commit()
    print(f"Inserted {len(records)} reviews")

    # Verification queries
    print("\n--- Verification ---")
    cur.execute("""
        SELECT b.bank_name, COUNT(r.review_id) as review_count, AVG(r.rating)::DECIMAL(3,2) as avg_rating
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
    """)
    for row in cur.fetchall():
        print(f"{row[0]}: {row[1]} reviews, avg rating {row[2]}")

    cur.close()
    conn.close()
    print("\n✅ Data loaded to PostgreSQL")

if __name__ == "__main__":
    main()