# scripts/visualize_insights.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# Create output folder
os.makedirs("reports/figures", exist_ok=True)

# Load data
df = pd.read_csv("data/enriched_reviews.csv")
print(f"Loaded {len(df)} reviews")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 1. Sentiment distribution by bank (stacked bar)
sentiment_counts = pd.crosstab(df['bank'], df['sentiment_label'])
ax = sentiment_counts.plot(kind='bar', stacked=True, colormap='RdYlGn', edgecolor='black')
plt.title('Sentiment Distribution by Bank', fontsize=14)
plt.xlabel('Bank')
plt.ylabel('Number of Reviews')
plt.legend(title='Sentiment')
plt.tight_layout()
plt.savefig('reports/figures/sentiment_distribution.png', dpi=300)
plt.close()
print("✓ Sentiment distribution saved")

# 2. Rating distribution per bank (histograms)
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, bank in enumerate(df['bank'].unique()):
    bank_df = df[df['bank'] == bank]
    rating_counts = bank_df['rating'].value_counts().sort_index()
    axes[i].bar(rating_counts.index, rating_counts.values, color='skyblue', edgecolor='black')
    axes[i].set_title(bank, fontsize=12)
    axes[i].set_xlabel('Rating')
    axes[i].set_ylabel('Count')
    axes[i].set_xticks(range(1,6))
plt.suptitle('Rating Distribution per Bank', fontsize=14)
plt.tight_layout()
plt.savefig('reports/figures/rating_distribution.png', dpi=300)
plt.close()
print("✓ Rating distribution saved")

# 3. Top themes (excluding 'Other')
theme_counts = df[df['identified_theme'] != 'Other']['identified_theme'].value_counts().head(8)
plt.figure(figsize=(10, 6))
theme_counts.plot(kind='barh', color='coral', edgecolor='black')
plt.title('Top 8 Themes (excluding Other)', fontsize=14)
plt.xlabel('Number of Reviews')
plt.tight_layout()
plt.savefig('reports/figures/top_themes.png', dpi=300)
plt.close()
print("✓ Top themes saved")

# 4. Word cloud of all reviews
all_text = ' '.join(df['review_text_cleaned'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis', max_words=100).generate(all_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in All Reviews', fontsize=14)
plt.tight_layout()
plt.savefig('reports/figures/wordcloud_all.png', dpi=300)
plt.close()
print("✓ Word cloud saved")

# 5. Average sentiment score by rating
avg_sentiment = df.groupby('rating')['sentiment_score'].mean()
plt.figure(figsize=(8, 5))
plt.plot(avg_sentiment.index, avg_sentiment.values, marker='o', linestyle='-', color='green', linewidth=2)
plt.title('Average Sentiment Score by Star Rating', fontsize=14)
plt.xlabel('Rating (stars)')
plt.ylabel('Average Sentiment Score')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('reports/figures/sentiment_vs_rating.png', dpi=300)
plt.close()
print("✓ Sentiment vs rating saved")

print("\n✅ All visualizations saved to reports/figures/")