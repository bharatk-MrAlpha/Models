# Technical Design

## Overview
The system collects tweets for Indian market hashtags between **09:00–15:30 IST**, processes/cleans them, computes **VADER** sentiment, aggregates into **15-minute buckets**, and emits **BUY/SELL/HOLD** signals with a confidence score.

## Key Choices
- **Twitter API v2** via Tweepy: reliable, handles rate limits via `wait_on_rate_limit=True`.
- **Combined hashtag query** to minimize API calls and avoid quota issues.
- **IST-first** time handling with lossless UTC conversions.
- **VADER** for fast lexical sentiment; can be swapped for FinBERT later.
- **Parquet** optional for compact storage; CSV universally readable.
- **Stateless CLI** to simplify scheduling and reproducibility.

## Data Model
Tweets schema:
- `username`: str
- `timestamp_ist`: tz-aware datetime (Asia/Kolkata)
- `content`: str
- `likes`, `retweets`, `replies`, `quotes`: int
- `mentions`: list[str]
- `hashtags`: list[str]
- `content_clean`: str
- `compound`: float [-1, 1]

Signals schema:
- `bucket`: 15-min start time (IST)
- `mean_compound`: float
- `count`: int
- `signal`: {BUY, SELL, HOLD}
- `confidence`: float (scaled |mean| × log(count+1))

## Algorithms
1. **Cleaning**: strip URLs, normalize whitespace.
2. **Sentiment**: VADER compound per tweet.
3. **Aggregation**: floor timestamps to 15-min, mean sentiment per bucket.
4. **Signal rule**:
   - BUY if mean > +0.05
   - SELL if mean < −0.05
   - HOLD otherwise

## Performance & Scalability
- Windowed collection minimizes calls; each page returns up to 100 tweets.
- Can parallelize across non-overlapping days.
- For 10× data: increase window size to 30 min with pagination, or use async collection.

## Error Handling
- Empty windows tolerated (skip).
- Parquet optional; falls back to CSV if `pyarrow` missing.
- Tweepy handles rate-limit sleeps automatically.

## Future Work
- Switch to **FinBERT** for finance sentiment.
- Entity linking to tickers, topic modeling.
- Online learning for dynamic thresholds.
