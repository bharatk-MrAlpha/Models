from __future__ import annotations
from typing import List, Dict
from datetime import datetime
import pytz
from twitter_client import make_client

def build_query(hashtags: list[str]) -> str:
    or_part = " OR ".join(hashtags)
    # lang:en and no retweets to reduce noise
    return f"({or_part}) lang:en -is:retweet"

def fetch_window(
    bearer_token: str,
    hashtags: list[str],
    start_utc: datetime,
    end_utc: datetime,
) -> List[Dict]:
    import tweepy
    client = make_client(bearer_token)
    ist = pytz.timezone("Asia/Kolkata")

    resp = client.search_recent_tweets(
        query=build_query(hashtags),
        start_time=start_utc,
        end_time=end_utc,
        max_results=100,
        expansions=["author_id"],
        user_fields=["username","public_metrics"],
        tweet_fields=["created_at","public_metrics","entities","lang","text"]
    )

    results: List[Dict] = []
    if not resp or not resp.data:
        return results

    # Map author_id -> username once per page
    user_map = {}
    if getattr(resp, "includes", None) and "users" in resp.includes:
        user_map = {u.id: u.username for u in resp.includes["users"]}

    for t in resp.data:
        ents = t.entities or {}
        #mentions = [m.get("username") for m in ents.get("mentions", [])]
        #hashtags_out = [h.get("tag") for h in ents.get("hashtags", [])]
        pm = t.public_metrics or {}

        results.append({
            "username": user_map.get(t.author_id),
            "timestamp_ist": t.created_at.astimezone(ist),
            "content": t.text,
            "likes": pm.get("like_count", 0),
            "retweets": pm.get("retweet_count", 0),
            "replies": pm.get("reply_count", 0),
            #"quotes": pm.get("quote_count", 0),
            #"mentions": mentions,
            #"hashtags": hashtags_out
        })
    return results
