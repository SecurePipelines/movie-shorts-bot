import feedparser
from datetime import datetime, timedelta, timezone
import os
import sys

CHANNEL_ID = os.getenv("CHANNEL_ID")

feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
feed = feedparser.parse(feed_url)

now = datetime.now(timezone.utc)
last_24_hours = now - timedelta(hours=24)

for entry in feed.entries:
    published_time = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S+00:00")
    published_time = published_time.replace(tzinfo=timezone.utc)

    if published_time >= last_24_hours:
        print(f"VIDEO_FOUND=true")
        print(f"TITLE={entry.title}")
        print(f"URL={entry.link}")
        sys.exit(0)

print("VIDEO_FOUND=false")