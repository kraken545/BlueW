#!/usr/bin/env python3
"""
BlueWave - Generador de videos cortos automatizado
Usa FFmpeg para crear videos promocionales tipo Reels/TikTok.
Requisito: ffmpeg instalado en el sistema
"""

import subprocess
import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets")

TEXTS = [
    "BlueWave - Curaçao Good Vibes",
    "El corazón de Curaçao en blockchain",
    "Descubre Curaçao con BlueWave",
    "Sun, Sea & BlueWave",
    "Barika Hel - El espíritu de Curaçao",
]

MUSIC_DIR = os.path.join(OUTPUT_DIR, "music")


def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.FileNotFoundError, subprocess.CalledProcessError):
        print("❌ FFmpeg no instalado. Instala con: sudo apt install ffmpeg")
        return False


def create_reel(
    image_path: str = None,
    text: str = None,
    audio_path: str = None,
    output_path: str = None,
    duration: int = 15,
):
    """Crea un video vertical tipo Reels/TikTok (1080x1920)."""
    if not check_ffmpeg():
        return None

    img = image_path or os.path.join(ASSETS_DIR, "logo-full.svg")
    txt = text or TEXTS[0]
    output = output_path or os.path.join(
        OUTPUT_DIR, f"reel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", img,
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-vf", (
            f"scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,"
            f"drawtext=text='{txt}':fontcolor=white:fontsize=48:"
            f"x=(w-text_w)/2:y=h-200:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf,"
            f"drawtext=text='$BLUEW':fontcolor=yellow:fontsize=36:"
            f"x=(w-text_w)/2:y=h-120:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
    ]

    if audio_path and os.path.exists(audio_path):
        cmd.extend(["-i", audio_path])
    else:
        # Silencio si no hay audio
        cmd.extend([
            "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=mono",
        ])

    cmd.append(output)

    print(f"🎬 Creando Reel...")
    subprocess.run(cmd, check=True)
    print(f"✅ Reel creado: {output}")
    return output


if __name__ == "__main__":
    create_reel()
