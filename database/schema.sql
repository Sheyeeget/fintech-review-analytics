-- Banks table
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(10) NOT NULL,
    sentiment_score FLOAT NOT NULL,
    identified_theme VARCHAR(100),
    source VARCHAR(50) DEFAULT 'Google Play',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_bank
        FOREIGN KEY (bank_id)
        REFERENCES banks(bank_id)
        ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);

-- Insert bank metadata (adjust app names as needed)
INSERT INTO banks (bank_name, app_name) VALUES
    ('Commercial Bank of Ethiopia', 'CBE Mobile Banking'),
    ('Bank of Abyssinia', 'BOA Mobile Banking'),
    ('Dashen Bank', 'Dashen Mobile Banking')
ON CONFLICT (bank_name) DO NOTHING;