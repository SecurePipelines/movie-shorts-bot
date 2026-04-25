import subprocess

def create_clips(input_video, clips=5, duration=30):
    print("✂️ Creating shorts...")

    outputs = []

    for i in range(clips):
        start = i * duration
        output = f"short_{i}.mp4"

        cmd = (
            f"ffmpeg -i {input_video} -ss {start} -t {duration} "
            f"-vf \"crop=ih*9/16:ih,scale=1080:1920\" "
            f"-c:a copy {output} -y"
        )

        subprocess.run(cmd, shell=True)
        outputs.append(output)

    return outputs