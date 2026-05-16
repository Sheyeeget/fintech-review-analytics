#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import PlayStoreScraper
from src.preprocessing import ReviewPreprocessor

def main():
    os.makedirs("data", exist_ok=True)
    
    print("Step 1: Scraping reviews...")
    scraper = PlayStoreScraper()
    raw_df = scraper.scrape_all_banks(reviews_per_bank=500)
    
    if raw_df.empty:
        print("No data scraped.")
        return
    
    raw_df.to_csv("data/raw_reviews.csv", index=False)
    
    print("Step 2: Preprocessing...")
    preprocessor = ReviewPreprocessor(raw_df)
    cleaned_df = preprocessor.preprocess()
    cleaned_df.to_csv("data/cleaned_reviews.csv", index=False)
    
    print("\nSummary:")
    print(cleaned_df['bank'].value_counts())
    print(f"Total reviews: {len(cleaned_df)}")
    print("✅ Task 1 complete.")

if __name__ == "__main__":
    main() 
