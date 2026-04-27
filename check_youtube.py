import requests
import re
import feedparser
import os

CHANNEL_HANDLE = "@souravjvlogs"
LAST_VIDEO_FILE = "last_video.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 🔹 Step 1: Get channel page
url = f"https://www.youtube.com/{CHANNEL_HANDLE}"
html = requests.get(url, headers=HEADERS).text

# 🔹 Step 2: Extract channel ID (externalId)
match = re.search(r'"externalId":"(UC[\w-]+)"', html)

if not match:
    print("❌ Could not extract channel ID")
    exit(1)

channel_id = match.group(1)
print("Channel ID:", channel_id)

# 🔹 Step 3: Convert to uploads playlist
playlist_id = "UU" + channel_id[2:]

# 🔹 Step 4: Fetch RSS
feed_url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"
feed = feedparser.parse(feed_url, request_headers=HEADERS)

if not feed.entries:
    print("❌ No videos found (check channel or feed)")
    exit(1)

latest = feed.entries[0]
video_id = latest.yt_videoid
title = latest.title
url = latest.link

print("Latest Video:", title)

# 🔹 Step 5: Compare with last stored video
if os.path.exists(LAST_VIDEO_FILE):
    with open(LAST_VIDEO_FILE, "r") as f:
        last_video = f.read().strip()
else:
    last_video = None

if video_id != last_video:
    print("VIDEO_FOUND=true")
    print(f"TITLE={title}")
    print(f"URL={url}")

    # Save latest video ID
    with open(LAST_VIDEO_FILE, "w") as f:
        f.write(video_id)
else:
    print("VIDEO_FOUND=false")