from __future__ import annotations
import re
import pandas as pd

URL_RE = re.compile(r"http\S+|www\.\S+")
WS_RE = re.compile(r"\s+")

def clean_text(s: str) -> str:
    s = URL_RE.sub(" ", s)
    s = WS_RE.sub(" ", s).strip()
    return s

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["content_clean"] = df["content"].astype(str).apply(clean_text)
    return df
