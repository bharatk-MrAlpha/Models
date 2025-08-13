from __future__ import annotations
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_interval_sentiment(sig: pd.DataFrame, out_dir: str, title: str = "Interval Sentiment (15m)") -> str:
    if sig.empty:
        return ""
    os.makedirs(out_dir, exist_ok=True)
    png_path = os.path.join(out_dir, "interval_sentiment.png")

    plt.figure()
    plt.plot(sig["bucket"], sig["mean_compound"])
    plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.xlabel("Time (IST)")
    plt.ylabel("Mean Compound Sentiment")
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    plt.close()
    return png_path

def plot_signal_counts(sig: pd.DataFrame, out_dir: str, title: str = "Signal Counts") -> str:
    if sig.empty:
        return ""
    os.makedirs(out_dir, exist_ok=True)
    png_path = os.path.join(out_dir, "signal_counts.png")

    counts = sig["signal"].value_counts()
    plt.figure()
    counts.plot(kind="bar")
    plt.title(title)
    plt.xlabel("Signal")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    plt.close()
    return png_path
