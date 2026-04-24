import subprocess, os

def create_video():
    os.makedirs("output", exist_ok=True)

    cmd = [
        "ffmpeg",
        "-i", "assets/bg.mp4",
        "-i", "output/voice.mp3",
        "-vf", "scale=1080:1920",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-y",
        "output/video.mp4"
    ]

    subprocess.run(cmd)
    return "output/video.mp4"