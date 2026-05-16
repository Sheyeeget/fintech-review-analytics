
import pandas as pd
import re

class ReviewPreprocessor:
    def __init__(self, df):
        self.df = df.copy()
        
    def remove_duplicates(self):
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=['review_text'])
        print(f"Removed {before - len(self.df)} duplicates")
        return self.df
    
    def handle_missing_values(self):
        before = len(self.df)
        self.df = self.df.dropna(subset=['review_text', 'rating'])
        if 'review_date' in self.df.columns:
            self.df['review_date'] = self.df['review_date'].fillna('2024-01-01')
        print(f"Removed {before - len(self.df)} rows with missing data")
        return self.df
    
    def normalize_dates(self):
        if 'review_date' in self.df.columns:
            self.df['review_date'] = pd.to_datetime(self.df['review_date'], errors='coerce').dt.strftime('%Y-%m-%d')
            self.df['review_date'] = self.df['review_date'].fillna('2024-01-01')
        return self.df
    
    def clean_text(self):
        def clean(text):
            if not isinstance(text, str):
                return ''
            text = re.sub(r'http\S+', '', text)
            text = re.sub(r'[^a-zA-Z\s]', ' ', text)
            text = text.lower()
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        self.df['review_text_cleaned'] = self.df['review_text'].apply(clean)
        return self.df
    
    def preprocess(self):
        print("=== Starting Preprocessing ===")
        self.remove_duplicates()
        self.handle_missing_values()
        self.normalize_dates()
        self.clean_text()
        print(f"Final rows: {len(self.df)}")
        return self.df