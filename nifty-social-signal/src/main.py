from __future__ import annotations
import argparse, os
from datetime import datetime
import pandas as pd
from config import load_settings
from utils import IST, iter_windows_utc
from collect import fetch_window
from preprocess import preprocess_df
from sentiment import add_sentiment
from signal_sa import interval_signals, combined_daily_signal
from plotting import plot_interval_sentiment, plot_signal_counts

def run(date_str: str|None):
    #load settings from env file
    settings = load_settings()
    day = datetime.now(IST) if (date_str in [None, "", "today"]) else IST.localize(datetime.fromisoformat(date_str))

    all_rows = []
    
    #get tweet data from free tweepy api
    for s_utc, e_utc in iter_windows_utc(day, settings.interval_minutes):
        rows = fetch_window(settings.bearer_token, settings.hashtags, s_utc, e_utc)
        all_rows.extend(rows)

    if not all_rows:
        print("No tweets collected. Exiting.")
        return
    
    df = pd.DataFrame(all_rows)
    df = preprocess_df(df) #preprocess all data
    df = add_sentiment(df) #do sentiment analysis with vader
    #create signal as per parameters set in env
    sig = interval_signals(df, settings.buy_threshold, settings.sell_threshold)

    # Output dirs
    out_dir = "data/output"
    os.makedirs(out_dir, exist_ok=True)
    ymd = day.astimezone(IST).strftime("%Y-%m-%d")
    day_dir = os.path.join(out_dir, ymd)
    os.makedirs(day_dir, exist_ok=True)
    tweets_csv = os.path.join(out_dir, f"tweets_{ymd}.csv")
    tweets_parquet = os.path.join(out_dir, f"tweets_{ymd}.parquet")
    sig_csv = os.path.join(out_dir, f"signals_{ymd}.csv")

    df.to_csv(tweets_csv, index=False, encoding="utf-8-sig")
    try:
        df.to_parquet(tweets_parquet, index=False)
    except Exception as e:
        print("Parquet save failed (install pyarrow).", e)

    sig.to_csv(sig_csv, index=False, encoding="utf-8-sig")

    # Combined daily signal
    combo = combined_daily_signal(sig, settings.buy_threshold, settings.sell_threshold)
    print(f"Combined Daily Signal: {combo['signal']} (mean={combo['mean']:.3f}, n={combo['count']})")

    # Plots
    if settings.make_plots:
        p1 = plot_interval_sentiment(sig, day_dir, title=f"Interval Sentiment {ymd}")
        p2 = plot_signal_counts(sig, day_dir, title=f"Signal Counts {ymd}")
        if p1: print(f"Wrote plot: {p1}")
        if p2: print(f"Wrote plot: {p2}")

    print(f"Saved {len(df)} tweets -> {tweets_csv}")
    print(f"Saved {len(sig)} intervals -> {sig_csv}")

def main():
    ap = argparse.ArgumentParser(description="NIFTY social sentiment signal generator")
    ap.add_argument("cmd", choices=["run"], help="Action")
    ap.add_argument("--date", default="today", help="IST date YYYY-MM-DD or 'today'")
    args = ap.parse_args()
    if args.cmd == "run":
        run(args.date)

if __name__ == "__main__":
    main()
