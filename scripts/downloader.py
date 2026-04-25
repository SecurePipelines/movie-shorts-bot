import subprocess
import json

def download_latest_video(channel_url):
    print("📥 Fetching latest video...")

    cmd = f"yt-dlp -j --playlist-items 1 {channel_url}"
    result = subprocess.check_output(cmd, shell=True).decode()

    data = json.loads(result.split("\n")[0])
    video_url = data["webpage_url"]

    print("⬇️ Downloading:", video_url)
    subprocess.run(f"yt-dlp -f mp4 -o video.mp4 {video_url}", shell=True)

    return "video.mp4"