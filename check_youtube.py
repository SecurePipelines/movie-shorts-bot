import requests
import re
import json
import os
import sys

CHANNEL_HANDLE = "@souravjvlogs"
LAST_VIDEO_FILE = "last_video.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

try:
    url = f"https://www.youtube.com/{CHANNEL_HANDLE}/videos"
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        print("❌ Failed to fetch page")
        print("VIDEO_FOUND=false")
        sys.exit(0)

    html = response.text

    # Extract ytInitialData JSON
    match = re.search(r'var ytInitialData = ({.*?});', html)

    if not match:
        print("❌ Could not extract video data")
        print("VIDEO_FOUND=false")
        sys.exit(0)

    data = json.loads(match.group(1))

    # Navigate JSON safely
    videos = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]\
        ["tabRenderer"]["content"]["richGridRenderer"]["contents"]

    # Find first video
    for item in videos:
        if "richItemRenderer" in item:
            video_data = item["richItemRenderer"]["content"]["videoRenderer"]
            video_id = video_data["videoId"]
            title = video_data["title"]["runs"][0]["text"]
            break

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    print("Latest Video:", title)

    # Check last processed
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