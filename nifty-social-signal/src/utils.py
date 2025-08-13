from __future__ import annotations
from datetime import datetime, timedelta, time
import pytz
from typing import Iterator, Tuple

IST = pytz.timezone("Asia/Kolkata")
UTC = pytz.UTC

def trading_window_ist(day_ist: datetime) -> tuple[datetime, datetime]:
    d = day_ist.astimezone(IST)
    start = IST.localize(datetime(d.year, d.month, d.day, 9, 0, 0))
    end   = IST.localize(datetime(d.year, d.month, d.day, 15, 30, 0))
    return start, end

def iter_windows_utc(day_ist: datetime, minutes: int) -> Iterator[tuple[datetime, datetime]]:
    start_ist, end_ist = trading_window_ist(day_ist)
    cur = start_ist
    delta = timedelta(minutes=minutes)
    while cur < end_ist:
        nxt = min(cur + delta, end_ist)
        yield cur.astimezone(UTC), nxt.astimezone(UTC)
        cur = nxt
