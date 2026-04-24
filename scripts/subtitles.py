import whisper

def format_time(t):
    hrs = int(t // 3600)
    mins = int((t % 3600) // 60)
    secs = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

def generate_subtitles(audio):
    model = whisper.load_model("base")
    result = model.transcribe(audio)

    path = "output/subtitles.srt"

    with open(path, "w") as f:
        for i, seg in enumerate(result["segments"]):
            f.write(f"{i+1}\n")
            f.write(f"{format_time(seg['start'])} --> {format_time(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")

    return path