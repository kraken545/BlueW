#!/usr/bin/env python3
"""
BlueWave - Generador automático de contenido promocional
Crea imágenes con overlay de texto y videos cortos para redes sociales.
Dependencias: pip install Pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont
import json
import random
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets")

MESSAGES = [
    "Good vibes from Curaçao 🌊",
    "BlueWave - El corazón de Curaçao",
    "Curaçao turismo, cultura y buena vibra",
    "Barika Hel volando sobre BlueWave",
    "Sun, sea & BlueWave",
    "Curaçao te espera",
    "BlueWave – Good vibes only",
    "Descubre Curaçao con BlueWave",
    "Isla de colores, token de corazón",
    "BlueWave: la vibe de Curaçao en blockchain",
]

HASHTAGS = [
    "#BlueWave #BLUEW #Curaçao #Curacao",
    "#BlueWave #Memecoin #Solana #Curaçao",
    "#Curaçao #GoodVibes #BlueWave #Crypto",
    "#BlueWave #BLUEW #SolanaSummer #Curaçao",
    "#Dushi #Curaçao #BlueWave #Token",
]


def create_promo_image(
    background_path: str = None,
    logo_path: str = None,
    message: str = None,
    output_path: str = None,
):
    """Crea una imagen promocional con overlay de texto."""
    size = (1080, 1080)

    img = Image.new("RGB", size, (0, 119, 182))

    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((600, 600))
        x = (size[0] - logo.width) // 2
        y = 100
        img.paste(logo, (x, y), logo)

    draw = ImageDraw.Draw(img)
    text = message or random.choice(MESSAGES)
    hashtag = random.choice(HASHTAGS)
    font_large = None
    font_small = None
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((size[0] - tw) // 2, 750), text, fill="white", font=font_large)

    bbox2 = draw.textbbox((0, 0), hashtag, font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((size[0] - tw2) // 2, 830), hashtag, fill="#FFD200", font=font_small)

    # BlueWave branding at bottom
    draw.text((30, 1000), "BlueWave", fill="#90E0EF", font=font_small)
    draw.text((30, 1035), "$BLUEW", fill="#FFD200", font=font_small)

    os.makedirs(os.path.dirname(output_path or "."), exist_ok=True)
    output = output_path or os.path.join(
        OUTPUT_DIR, f"promo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )
    img.save(output)
    print(f"✅ Imagen creada: {output}")
    return output


if __name__ == "__main__":
    logo = os.path.join(ASSETS_DIR, "logo-full.svg")
    if not os.path.exists(logo):
        print("⚠️ Logo SVG no encontrado, se usará solo texto")
        logo = None
    create_promo_image(logo_path=logo)
