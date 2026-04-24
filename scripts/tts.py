import requests, os

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

def generate_voice(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.9
        }
    }

    r = requests.post(url, json=data, headers=headers)

    os.makedirs("output", exist_ok=True)

    with open("output/voice.mp3", "wb") as f:
        f.write(r.content)

    return "output/voice.mp3"