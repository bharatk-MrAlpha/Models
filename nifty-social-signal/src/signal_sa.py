from __future__ import annotations
import pandas as pd
import numpy as np

def bucketize_to_15min(df: pd.DataFrame, ts_col: str = "timestamp_ist") -> pd.DataFrame:
    df = df.copy()
    df["bucket"] = pd.to_datetime(df[ts_col]).dt.floor("15min")
    return df

def interval_signals(df: pd.DataFrame, buy_t: float, sell_t: float) -> pd.DataFrame:
    df = bucketize_to_15min(df)
    agg = df.groupby("bucket").agg(
        mean_compound=("compound","mean"),
        count=("compound","count")
    ).reset_index()

    def decide(x):
        if x > buy_t: return "BUY"
        if x < sell_t: return "SELL"
        return "HOLD"

    agg["signal"] = agg["mean_compound"].apply(decide)
    # Confidence: scale |mean| by log(count+1)
    if not agg.empty:
        m = agg["mean_compound"].abs()
        m = (m - m.min()) / (m.max() - m.min() + 1e-9)
        agg["confidence"] = (m * np.log1p(agg["count"])).round(3)
    else:
        agg["confidence"] = []
    return agg

def combined_daily_signal(sig: pd.DataFrame, buy_t: float, sell_t: float) -> dict:
    if sig.empty:
        return {"signal": "HOLD", "mean": 0.0, "count": 0}
    mean = sig["mean_compound"].mean()
    cnt = sig["count"].sum()
    if mean > buy_t:
        s = "BUY"
    elif mean < sell_t:
        s = "SELL"
    else:
        s = "HOLD"
    return {"signal": s, "mean": float(mean), "count": int(cnt)}
