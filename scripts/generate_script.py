import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_caption(topic):
    prompt = f"""
    Create a viral YouTube Shorts script for: {topic}

    Format:
    Hook (1 line)
    Story (2-3 lines)
    CTA (1 line)

    Add 3 hashtags.
    Keep under 80 words.
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API failed: {e}")
        # Fallback script
        return f"Hook: Discover the epic {topic}!\nStory: In this thrilling scene, heroes clash in an unforgettable battle.\nCTA: Like and subscribe for more movie magic!\n#MovieShorts #ActionScene #Cinema"