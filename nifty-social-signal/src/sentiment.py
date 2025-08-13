from __future__ import annotations
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

# Download NLTK VADER lexicon
import nltk
nltk.download('vader_lexicon')

def add_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    sia = SentimentIntensityAnalyzer()
    df["compound"] = df["content_clean"].apply(lambda x: sia.polarity_scores(x)["compound"])
    return df
