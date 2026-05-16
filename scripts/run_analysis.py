#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.sentiment_analyzer import SentimentAnalyzer
from src.thematic_analyzer import ThematicAnalyzer

def main():
    print("="*60)
    print("Task 2: Sentiment and Thematic Analysis")
    print("="*60)

    df = pd.read_csv("data/cleaned_reviews.csv")
    print(f"Loaded {len(df)} reviews")

    # Sentiment
    sentiment = SentimentAnalyzer()
    df = sentiment.add_sentiment(df)

    # Thematic
    thematic = ThematicAnalyzer()
    df = thematic.analyze_themes(df)

    # Save enriched data
    df.to_csv("data/enriched_reviews.csv", index=False)
    print("\n✓ Enriched data saved to data/enriched_reviews.csv")

    # Summary
    print("\n--- Sentiment by Bank ---")
    print(pd.crosstab(df['bank'], df['sentiment_label'], normalize='index'))

    print("\n--- Top Themes Overall ---")
    print(df['identified_theme'].value_counts().head(10))

if __name__ == "__main__":
    main()