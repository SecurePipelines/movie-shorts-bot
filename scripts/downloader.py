import os
import subprocess
import json
import tempfile


def _build_cookies_args():
    cookies_env = os.environ.get("YTDLP_COOKIES")
    cookies_file = os.environ.get("YTDLP_COOKIES_FILE")

    if cookies_env:
        tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
        tmp.write(cookies_env)
        tmp.close()
        return ["--cookies", tmp.name]

    if cookies_file and os.path.isfile(cookies_file):
        return ["--cookies", cookies_file]

    return []


def download_latest_video(channel_url):
    print("📥 Fetching latest video...")

    cookies_args = _build_cookies_args()
    cmd = ["yt-dlp", *cookies_args, "-j", "--playlist-items", "1", channel_url]
    result = subprocess.check_output(cmd).decode()

    data = json.loads(result.splitlines()[0])
    video_url = data["webpage_url"]

    print("⬇️ Downloading:", video_url)
    subprocess.run(["yt-dlp", *cookies_args, "-f", "mp4", "-o", "video.mp4", video_url], check=True)

    return "video.mp4"