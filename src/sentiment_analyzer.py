"""
Sentiment analysis using DistilBERT transformer model.
Classifies reviews as POSITIVE or NEGATIVE with confidence score.
"""
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from transformers import pipeline
import pandas as pd
from tqdm import tqdm
import torch

class SentimentAnalyzer:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        print(f"Loading sentiment model: {model_name}")
        self.classifier = pipeline(
            "sentiment-analysis",
            model=model_name,
            device=0 if torch.cuda.is_available() else -1
        )
        print("✓ Model loaded")

    def classify_batch(self, texts, batch_size=32):
        results = []
        for i in tqdm(range(0, len(texts), batch_size), desc="Classifying sentiment"):
            batch = texts[i:i+batch_size]
            outputs = self.classifier(batch, truncation=True, max_length=512)
            for out in outputs:
                label = 'POSITIVE' if out['label'] == 'POSITIVE' else 'NEGATIVE'
                results.append({'sentiment_label': label, 'sentiment_score': out['score']})
        return pd.DataFrame(results)

    def add_sentiment(self, df):
        texts = df['review_text_cleaned'].fillna('').tolist()
        sentiment_df = self.classify_batch(texts)
        df['sentiment_label'] = sentiment_df['sentiment_label']
        df['sentiment_score'] = sentiment_df['sentiment_score']
        return df