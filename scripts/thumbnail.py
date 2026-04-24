from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail(text):
    os.makedirs("output", exist_ok=True)

    img = Image.new("RGB", (1280, 720), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("assets/font.ttf", 70)

    draw.text((100, 300), text[:40], font=font, fill=(255, 255, 0))

    path = "output/thumb.jpg"
    img.save(path)

    return path