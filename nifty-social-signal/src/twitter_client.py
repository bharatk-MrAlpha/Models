from __future__ import annotations
import tweepy

def make_client(bearer_token: str) -> tweepy.Client:
    # wait_on_rate_limit=True will auto-sleep on 429s
    return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
