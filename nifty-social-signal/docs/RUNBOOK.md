# Runbook

## Prereqs
- Python 3.10+
- Twitter API v2 Bearer Token

## One-time setup
```bash
./setup.sh
cp .env.example .env  # put your BEARER_TOKEN
```

## Run for today (IST)
```bash
python src/main.py run --date today
```

## Run for specific date
```bash
python src/main.py run --date 2025-08-13
```

## Outputs
- `data/output/tweets_YYYY-MM-DD.csv|.parquet`
- `data/output/signals_YYYY-MM-DD.csv`

## Troubleshooting
- **429 Rate Limit**: reduce intervals, or run less frequently.
- **Parquet error**: `pip install pyarrow`.
- **Empty outputs**: Try a different date/time; some windows may be sparse.
