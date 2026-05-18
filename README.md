# Fintech Review Analytics

Analyzing Google Play Store reviews for Ethiopian banks (CBE, BOA, Dashen).

## Pipeline Overview

1. **Scrape** reviews (real + synthetic fallback) → `data/cleaned_reviews.csv`
2. **Analyze** sentiment (DistilBERT) and themes (TF‑IDF keywords) → `data/enriched_reviews.csv`
3. **Load** into PostgreSQL (`bank_reviews` database)
4. **Visualize** → plots in `reports/figures/`

## Scraping Methodology

| Bank                      | App ID (Package Name)                 | Real reviews | Synthetic (padding) | Final |
|---------------------------|---------------------------------------|--------------|---------------------|-------|
| Bank of Abyssinia         | `com.boa.apollo`                      | 405          | trimmed to 400      | 400   |
| Dashen Bank               | `com.cr2.amolelight`                  | 383          | 17                  | 400   |
| Commercial Bank of Ethiopia | `com.combanketh.mb.next`           | 0            | 400                 | 400   |

- **Date range:** Last 500 reviews per app (or all available).
- **Language/Country:** `lang='en'`, `country='et'`.
- **Limitation:** CBE app returned zero written reviews; synthetic data generated using same rating distribution as peers, clearly marked in `source` column.

## Data Dictionary

### `cleaned_reviews.csv` (after Task 1)
- `review_text`, `rating` (1‑5), `review_date` (YYYY‑MM‑DD), `bank`, `source`, `review_text_cleaned`

### `enriched_reviews.csv` (after Task 2)
- All above + `sentiment_label` (POSITIVE/NEGATIVE), `sentiment_score`, `identified_theme`

## Running the Pipeline

### Prerequisites
- Conda environment: `conda create --name fintech-reviews python=3.12 -y`
- Activate: `conda activate fintech-reviews`
- Install: `conda install -c conda-forge pandas numpy scikit-learn matplotlib seaborn nltk psycopg2 sqlalchemy pytest python-dotenv tqdm wordcloud pytorch cpuonly -y`
- Then: `pip install google-play-scraper spacy transformers && python -m spacy download en_core_web_sm`

### Execution
```bash
python scripts/collect_data.py          # Task 1
python scripts/run_analysis.py          # Task 2 (sentiment + themes)
python scripts/load_to_db.py            # Task 3 (PostgreSQL)
python scripts/visualize_insights.py    # Task 4 (plots)