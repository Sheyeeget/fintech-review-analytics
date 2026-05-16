"""
Google Play Store scraper for Ethiopian bank app reviews.
Handles multiple app IDs, fallbacks, and synthetic data generation if needed.
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import time
import logging
import random
import datetime
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PlayStoreScraper:
    """Robust scraper with fallback IDs and synthetic generation."""
    
    # Bank names and their possible app IDs (first one is primary)
    BANK_APPS: Dict[str, List[str]] = {
        "Commercial Bank of Ethiopia": [
            "prod.cbe.birr",          # CBEBirr Plus – often has reviews
            "com.combanketh.mb.next", # Current main app (returned 0 for you)
            "com.combanketh.mobilebanking"  # Older version
        ],
        "Bank of Abyssinia": ["com.boa.apollo"],
        "Dashen Bank": ["com.cr2.amolelight"]
    }
    
    def __init__(self, lang: Optional[str] = 'en', country: Optional[str] = 'et'):
        self.lang = lang
        self.country = country
        
    def scrape_reviews(self, app_name: str, app_ids: List[str], target_count: int = 500) -> pd.DataFrame:
        """
        Try multiple app IDs for a bank; returns first successful one.
        If all fail, returns empty DataFrame.
        """
        for app_id in app_ids:
            logging.info(f"Trying {app_name} with ID: {app_id}")
            df = self._try_scrape(app_name, app_id, target_count)
            if not df.empty:
                logging.info(f"✓ Success with {app_id}: {len(df)} reviews")
                return df
            logging.warning(f"✗ Failed with {app_id}")
        return pd.DataFrame()
    
    def _try_scrape(self, app_name: str, app_id: str, count: int) -> pd.DataFrame:
        """Attempt to scrape using specific app ID, with and without language filters."""
        # First attempt with original lang/country
        try:
            result, _ = reviews(app_id, lang=self.lang, country=self.country, sort=Sort.NEWEST, count=count)
            if result:
                return self._to_dataframe(result, app_name)
        except Exception as e:
            logging.debug(f"Error with lang/country: {e}")
        
        # Second attempt without language/country (to catch reviews in any language)
        try:
            result, _ = reviews(app_id, sort=Sort.NEWEST, count=count)
            if result:
                logging.info(f"Success without lang/country filter for {app_id}")
                return self._to_dataframe(result, app_name)
        except Exception as e:
            logging.debug(f"Error without filters: {e}")
        
        return pd.DataFrame()
    
    def _to_dataframe(self, result: List[dict], app_name: str) -> pd.DataFrame:
        df = pd.DataFrame(result)
        df['bank'] = app_name
        df['source'] = 'Google Play'
        df.rename(columns={'content': 'review_text', 'score': 'rating', 'at': 'review_date'}, inplace=True)
        df = df[['review_text', 'rating', 'review_date', 'bank', 'source']]
        return df
    
    def scrape_all_banks(self, reviews_per_bank: int = 500) -> pd.DataFrame:
        all_dfs = []
        for bank_name, app_ids in self.BANK_APPS.items():
            logging.info(f"\n=== Processing {bank_name} ===")
            df = self.scrape_reviews(bank_name, app_ids, reviews_per_bank)
            if df.empty:
                logging.error(f"❌ Could not scrape any reviews for {bank_name}. Generating synthetic data.")
                df = self._generate_synthetic_data(bank_name, reviews_per_bank)
            else:
                # If we got fewer than target, top up with synthetic (for CBE/Dashen edge case)
                if len(df) < reviews_per_bank and bank_name != "Bank of Abyssinia":
                    needed = reviews_per_bank - len(df)
                    logging.info(f"Only {len(df)} real reviews, generating {needed} synthetic to reach {reviews_per_bank}.")
                    synthetic_df = self._generate_synthetic_data(bank_name, needed)
                    df = pd.concat([df, synthetic_df], ignore_index=True)
            all_dfs.append(df)
            time.sleep(2)
        
        combined = pd.concat(all_dfs, ignore_index=True)
        logging.info(f"\n✅ Total reviews collected: {len(combined)}")
        return combined
    
    def _generate_synthetic_data(self, bank_name: str, n: int) -> pd.DataFrame:
        """Generate realistic reviews for a bank (used as fallback)."""
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=365)
        ratings = [1,2,3,4,5]
        rating_weights = [0.15,0.10,0.15,0.25,0.35]
        
        phrases = {
            'positive': [
                "Very reliable app, transfers are instant.",
                "Love the new interface, much cleaner.",
                "Customer support helped me quickly.",
                "Best banking app in Ethiopia.",
                "Biometric login works perfectly."
            ],
            'negative': [
                "OTP takes forever to arrive.",
                "App crashes when I try to pay bills.",
                "Login error almost every time.",
                "Slow loading screens.",
                "Transaction failed three times today."
            ],
            'feature': [
                "Please add fingerprint login.",
                "Would like to see a dark mode.",
                "Add QR code payment feature.",
                "Integrate savings goals.",
                "Make it easier to find transaction history."
            ]
        }
        
        data = []
        for _ in range(n):
            rating = random.choices(ratings, weights=rating_weights)[0]
            if rating >= 4:
                bucket = random.choices(['positive','feature'], weights=[0.7,0.3])[0]
            else:
                bucket = random.choices(['negative','feature'], weights=[0.8,0.2])[0]
            text = random.choice(phrases[bucket])
            rand_days = random.randint(0,365)
            review_date = start_date + datetime.timedelta(days=rand_days)
            data.append({
                'review_text': text,
                'rating': rating,
                'review_date': review_date.strftime('%Y-%m-%d'),
                'bank': bank_name,
                'source': 'Synthetic (generated)'
            })
        return pd.DataFrame(data)