from trending import get_trending_topics
from generate_script import generate_caption
from tts import generate_voice
from create_video import create_video
from subtitles import generate_subtitles
from thumbnail import create_thumbnail
from upload import upload_video
import os

def run():
    topic = get_trending_topics()[0]
    print("Topic:", topic)

    script = generate_caption(topic)

    audio = generate_voice(script)
    video = create_video()
    generate_subtitles(audio)

    os.system("ffmpeg -i output/video.mp4 -vf subtitles=output/subtitles.srt output/final.mp4")

    thumb = create_thumbnail(topic)

    upload_video("output/final.mp4", topic, script)

if __name__ == "__main__":
    run()