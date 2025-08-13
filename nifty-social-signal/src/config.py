from dataclasses import dataclass
import os

@dataclass
class Settings:
    bearer_token: str
    hashtags: list[str]
    interval_minutes: int = 15
    buy_threshold: float = 0.05
    sell_threshold: float = -0.05
    make_plots: bool = True

def load_settings() -> Settings:
    from dotenv import load_dotenv
    load_dotenv()

    token = os.getenv("BEARER_TOKEN", "").strip()
    if not token:
        raise ValueError("Missing BEARER_TOKEN in environment (.env).")

    hashtags_env = os.getenv("HASHTAGS", "#nifty50,#sensex,#banknifty,#intraday")
    tags = [t.strip() for t in hashtags_env.split(",") if t.strip()]

    interval = int(os.getenv("INTERVAL_MINUTES", "15"))
    buy_t = float(os.getenv("BUY_THRESHOLD", "0.05"))
    sell_t = float(os.getenv("SELL_THRESHOLD", "-0.05"))
    make_plots = os.getenv("MAKE_PLOTS", "true").lower() == "true"

    return Settings(
        bearer_token=token,
        hashtags=tags,
        interval_minutes=interval,
        buy_threshold=buy_t,
        sell_threshold=sell_t,
        make_plots=make_plots,
    )
load_settings()