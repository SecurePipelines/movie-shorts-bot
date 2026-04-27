import requests
import re
import feedparser
import os
import sys

CHANNEL_HANDLE = "@souravjvlogs"
LAST_VIDEO_FILE = "last_video.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # Step 1: Get channel page
    url = f"https://www.youtube.com/{CHANNEL_HANDLE}"
    html = requests.get(url, headers=HEADERS, timeout=10).text

    match = re.search(r'"externalId":"(UC[\w-]+)"', html)

    if not match:
        print("❌ Channel ID not found")
        print("VIDEO_FOUND=false")
        sys.exit(0)

    channel_id = match.group(1)
    print("Channel ID:", channel_id)

    # Step 2: Convert to playlist
    playlist_id = "UU" + channel_id[2:]

    # Step 3: Fetch RSS using requests (IMPORTANT FIX)
    feed_url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"

    response = requests.get(feed_url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        print("❌ RSS fetch failed:", response.status_code)
        print("VIDEO_FOUND=false")
        sys.exit(0)

    feed = feedparser.parse(response.text)

    if not feed.entries:
        print("❌ RSS parsed but no entries (likely blocked earlier)")
        print("VIDEO_FOUND=false")
        sys.exit(0)

    latest = feed.entries[0]

    video_id = latest.get("yt_videoid", "")
    title = latest.get("title", "")
    video_url = latest.get("link", "")

    if not video_id:
        print("❌ Invalid video data")
        print("VIDEO_FOUND=false")
        sys.exit(0)

    # Step 4: Check last video
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r") as f:
            last_video = f.read().strip()
    else:
        last_video = None

    if video_id != last_video:
        print("VIDEO_FOUND=true")
        print(f"TITLE={title}")
        print(f"URL={video_url}")

        with open(LAST_VIDEO_FILE, "w") as f:
            f.write(video_id)
    else:
        print("VIDEO_FOUND=false")

except Exception as e:
    print("❌ ERROR:", str(e))
    print("VIDEO_FOUND=false")
    sys.exit(0)