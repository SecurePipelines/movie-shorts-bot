import json
from downloader import download_latest_video
from cutter import create_clips
from uploader import upload_video

def main():
    print("🚀 Starting Shorts Bot...")

    with open("config.json") as f:
        config = json.load(f)

    video = download_latest_video(config["channel_url"])

    clips = create_clips(
        video,
        config["clips_per_video"],
        config["clip_duration"]
    )

    for i, clip in enumerate(clips):
        title = f"🔥 Short #{i+1} | Must Watch! #shorts"
        upload_video(clip, title)

if __name__ == "__main__":
    main()