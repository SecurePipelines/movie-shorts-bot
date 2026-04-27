import requests
import re
import json
import os
import sys
import yt_dlp

# =========================
# CONFIG
# =========================
CHANNEL_HANDLE = "@souravjvlogs"
LAST_VIDEO_FILE = "last_video.txt"
DOWNLOAD_FOLDER = "downloads"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# =========================
# STEP 1: GET LATEST VIDEO
# =========================
def get_latest_video():
    url = f"https://www.youtube.com/{CHANNEL_HANDLE}/videos"
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        print("❌ Failed to fetch channel page")
        return None, None, None

    html = response.text

    # Extract ytInitialData JSON
    match = re.search(r'var ytInitialData = ({.*?});', html)

    if not match:
        print("❌ Could not extract video data")
        return None, None, None

    data = json.loads(match.group(1))

    try:
        videos = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]\
            ["tabRenderer"]["content"]["richGridRenderer"]["contents"]

        for item in videos:
            if "richItemRenderer" in item:
                video_data = item["richItemRenderer"]["content"]["videoRenderer"]
                video_id = video_data["videoId"]
                title = video_data["title"]["runs"][0]["text"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                return video_id, title, video_url
    except Exception:
        print("❌ Error parsing video data")

    return None, None, None


# =========================
# STEP 2: CHECK NEW VIDEO
# =========================
def is_new_video(video_id):
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r") as f:
            last_video = f.read().strip()
    else:
        last_video = None

    return video_id != last_video


# =========================
# STEP 3: SAVE VIDEO ID
# =========================
def save_video_id(video_id):
    with open(LAST_VIDEO_FILE, "w") as f:
        f.write(video_id)


# =========================
# STEP 4: DOWNLOAD VIDEO
# =========================
def download_video(video_url):
    print("⬇️ Downloading video...")

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': 'best[height<=720]',  # limit size for CI
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


# =========================
# MAIN FLOW
# =========================
def main():
    video_id, title, video_url = get_latest_video()

    if not video_id:
        print("VIDEO_FOUND=false")
        sys.exit(0)

    print(f"Latest Video: {title}")

    if is_new_video(video_id):
        print("VIDEO_FOUND=true")
        print(f"TITLE={title}")
        print(f"URL={video_url}")

        download_video(video_url)
        save_video_id(video_id)
    else:
        print("VIDEO_FOUND=false")


if __name__ == "__main__":
    main()