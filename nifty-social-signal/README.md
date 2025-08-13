# nifty-social-signal

Sentiment-driven trading signal generator for Indian market hashtags (`#nifty50`, `#sensex`, `#banknifty`, `#intraday`) using **Twitter API v2**.

- Collects tweets between **9:00 AM IST** and **3:30 PM IST** in **15-minute intervals**.
- Extracts username, timestamp (IST), content, engagement metrics, mentions, and hashtags.
- Scores sentiment with **VADER** and aggregates to interval-level signals.
- Outputs BUY/SELL/HOLD with confidence and lightweight plots.

> ✅ No paid API required beyond standard Twitter API v2 bearer token.  
> ⚠️ Be mindful of rate limits; this repo batches requests efficiently.

---

## Quick start

### 1) Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; import ssl; ssl._create_default_https_context = ssl._create_unverified_context; import nltk; nltk.download('vader_lexicon')"
```

### 2) Configure
Create `.env` from example and set your **Twitter Bearer Token**:
```bash
cp .env.example .env
# edit .env to set BEARER_TOKEN="YOUR_TOKEN"
```

### 3) Run a full-day collection (today IST)
```bash
python src/main.py run --date today
```

Or specify a date (YYYY-MM-DD in IST):
```bash
python src/main.py run --date 2025-08-13
```

Outputs will be in `data/output/`:
- `tweets_YYYY-MM-DD.csv` & `.parquet`
- `signals_YYYY-MM-DD.csv`

---

## Project structure

```
nifty-social-signal/
├── README.md
├── requirements.txt
├── .env.example
├── setup.sh
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── twitter_client.py
│   ├── utils.py
│   ├── collect.py
│   ├── preprocess.py
│   ├── sentiment.py
│   ├── signal.py
│   └── main.py
├── data/
│   ├── sample/
│   │   ├── sample_tweets.csv
│   │   └── sample_signals.csv
│   └── output/   # created at runtime
└── docs/
    ├── TECHNICAL_DESIGN.md
    └── RUNBOOK.md
```

---

## Signals (high level)

- Compute VADER compound score per tweet.
- Aggregate by 15-min bucket (IST), compute mean & CI.
- Rule:
  - **BUY** if mean > +0.05
  - **SELL** if mean < −0.05
  - **HOLD** otherwise
- Confidence = normalized |mean| with tweet count weighting.

---

## Notes

- If you hit rate limits, reduce interval span, or skip low-volume windows.
- Combine hashtags to minimize calls.
- This repo is education-focused; adapt thresholds for live trading.


---

## Configuration

You can tune the signal thresholds and plotting via `.env`:

```env
BUY_THRESHOLD=0.05
SELL_THRESHOLD=-0.05
MAKE_PLOTS=true
```

Higher |thresholds| make signals rarer but higher-confidence.

## Combined daily signal

Along with 15-minute interval signals, the app prints a **combined daily signal**:
```
Combined Daily Signal: BUY (mean=0.087, n=942)
```
This is the mean of interval sentiment vs thresholds.

## GitHub Actions (optional)

A ready workflow runs on weekdays ~10:05 IST (04:35 UTC).  
Add your bearer token as a repo secret named **`BEARER_TOKEN`**.

```text
Settings → Secrets and variables → Actions → New repository secret
Name: BEARER_TOKEN
Value: <your token>
```

Artifacts (CSV + PNG plots) will be attached to each run.

