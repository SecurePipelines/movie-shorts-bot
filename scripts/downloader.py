import os
import subprocess
import json
import tempfile
from urllib.parse import urlparse, parse_qs

from google.oauth2.credentials import Credentials
import googleapiclient.discovery

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]


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


def _is_youtube_video_url(url):
    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if host.endswith("youtube.com"):
        if parsed.path == "/watch" and "v=" in parsed.query:
            return True
        if parsed.path.startswith("/shorts/"):
            return True
    if host in ("youtu.be", "www.youtu.be"):
        return True

    return False


def _get_video_url_from_input(url):
    if not _is_youtube_video_url(url):
        return None

    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if host.endswith("youtube.com"):
        if parsed.path == "/watch":
            query = parse_qs(parsed.query)
            video_id = query.get("v", [None])[0]
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"
        if parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/", 1)[1].strip("/")
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"

    if host in ("youtu.be", "www.youtu.be"):
        video_id = parsed.path.strip("/")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    return None


def download_latest_video(channel_url):
    print("📥 Fetching latest video...")

    cookies_args = _build_cookies_args()
    js_args = ["--js-runtimes", "deno"]

    video_url = _get_video_url_from_input(channel_url)
    if video_url:
        print("Direct video URL detected:", video_url)
    else:
        cmd = ["yt-dlp", *cookies_args, *js_args, "-j", "--playlist-items", "1", channel_url]

        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
        except subprocess.CalledProcessError as exc:
            print("yt-dlp failed with output:\n", exc.output.decode(errors="replace"))
            raise

        data = json.loads(result.splitlines()[0])
        video_url = data["webpage_url"]

    print("⬇️ Downloading:", video_url)
    try:
        subprocess.run(
            ["yt-dlp", *cookies_args, *js_args, "--no-playlist", "-f", "mp4", "-o", "video.mp4", video_url],
            check=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )
    except subprocess.CalledProcessError as exc:
        output = exc.stdout.decode(errors="replace") if exc.stdout else ""
        print("yt-dlp failed while downloading:\n", output)
        if "Sign in to confirm you’re not a bot" in output:
            raise RuntimeError(
                "This YouTube video requires cookies/authentication. "
                "Set the YTDLP_COOKIES secret with exported browser cookies, "
                "or use a publicly accessible video URL."
            ) from exc
        raise

    return "video.mp4"