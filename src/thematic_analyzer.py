"""
Improved thematic analysis with expanded banking‑specific keywords.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
import spacy

class ThematicAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except:
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
            self.nlp = spacy.load('en_core_web_sm')

        # Expanded theme keywords (more synonyms and common banking terms)
        self.themes = {
            'Transaction Performance': [
                'slow', 'fast', 'speed', 'quick', 'instant', 'timeout', 'transfer', 'payment',
                'send money', 'receive', 'transaction', 'processing', 'load', 'response time',
                'delay', 'lag', 'wait', 'takes forever', 'instant'
            ],
            'Account Access': [
                'login', 'access', 'log in', 'sign in', 'password', 'otp', 'verification',
                'authenticate', 'can\'t log', 'unable to access', 'locked out', 'reset',
                'two factor', '2fa', 'fingerprint', 'biometric', 'face id', 'pin'
            ],
            'Reliability / Crashes': [
                'crash', 'error', 'bug', 'fail', 'broken', 'stuck', 'freeze', 'close',
                'shut down', 'not working', 'doesn\'t work', 'issue', 'problem', 'glitch',
                'force close', 'unresponsive'
            ],
            'Feature Request': [
                'add', 'feature', 'wish', 'suggest', 'improve', 'implement', 'include',
                'would be nice', 'need', 'missing', 'enhance', 'upgrade', 'new version',
                'dark mode', 'qr code', 'budget', 'savings', 'export', 'statement'
            ],
            'UI & Design': [
                'interface', 'design', 'ui', 'navigation', 'layout', 'look', 'appearance',
                'modern', 'outdated', 'cluttered', 'clean', 'intuitive', 'user friendly',
                'font', 'color', 'button', 'menu'
            ],
            'Customer Support': [
                'support', 'customer service', 'help', 'assistance', 'complaint', 'resolve',
                'call', 'chat', 'agent', 'representative', 'respond', 'reply', 'ticket'
            ],
            'Security': [
                'secure', 'security', 'safe', 'trust', 'protection', 'fraud', 'privacy',
                'encrypt', 'hack', 'scam', 'unauthorized', 'stolen', 'risk'
            ]
        }

    def classify_theme(self, text):
        if not isinstance(text, str):
            return 'Other'
        text_lower = text.lower()
        for theme, keywords in self.themes.items():
            for kw in keywords:
                if kw in text_lower:
                    return theme
        return 'Other'

    def extract_keywords_tfidf(self, texts, n=20):
        vectorizer = TfidfVectorizer(max_features=200, stop_words='english', ngram_range=(1,2))
        tfidf = vectorizer.fit_transform(texts)
        scores = tfidf.sum(axis=0).A1
        words = vectorizer.get_feature_names_out()
        top_idx = scores.argsort()[-n:][::-1]
        return [(words[i], scores[i]) for i in top_idx if scores[i] > 0]

    def analyze_themes(self, df):
        print("\n=== Running Improved Thematic Analysis ===")
        df['identified_theme'] = df['review_text_cleaned'].apply(self.classify_theme)
        print("\nTheme distribution:")
        print(df['identified_theme'].value_counts())
        print(f"\nPercentage covered (non-Other): {100 * (1 - df['identified_theme'].value_counts(normalize=True).get('Other', 0)):.1f}%")
        return df