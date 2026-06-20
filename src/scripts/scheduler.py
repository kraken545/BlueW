#!/usr/bin/env python3
"""
BlueWave - Programador de contenido automático
Ejecuta cada N horas: genera contenido y lo publica en redes.
Uso: nohup python3 src/scripts/scheduler.py &
"""

import os
import sys
import time
import random
import subprocess
from datetime import datetime

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
INTERVAL_HOURS = 6
INTERVAL_SECONDS = INTERVAL_HOURS * 3600

MESSAGES = [
    "Sun, sea, and BlueWave 🌊 Good vibes from Curaçao! #BlueWave #BLUEW",
    "El corazón de Curaçao late en blockchain 💙 #BlueWave #Curaçao",
    "Barika Hel, el espíritu de la isla, vuela con BlueWave 🦜 #BlueWave",
    "Curaçao turismo, cultura, y buena vibra 🌴 #BlueWave #Curaçao",
    "BlueWave - Representando la buena vibra de Curaçao 🌊 #BLUEW",
    "Descubre la magia de Curaçao con BlueWave ✨ #Curaçao #BlueWave",
    "Good vibes only from the island of Curaçao 🌊 $BLUEW",
    "BlueWave: where Caribbean vibes meet Solana ☀️ #BlueWave",
    "From Curaçao with love 💙 $BLUEW #Curaçao #Memecoin",
    "Una ola de buena vibra desde Curaçao 🌊 #BlueWave #BLUEW",
]


def run_script(script_name: str, *args):
    path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(path):
        print(f"⚠️ Script no encontrado: {path}")
        return
    cmd = [sys.executable, path, *args]
    print(f"▶️ Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=os.path.dirname(SCRIPTS_DIR))


def generate_and_post():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*50}")
    print(f"🕐 Scheduler ejecutándose: {now}")
    print(f"{'='*50}")

    # Generar imagen promocional
    run_script("generate_content.py")

    # Generar video Reel (cada 4 ejecuciones, una vez al día)
    if random.randint(1, 4) == 1:
        run_script("generate_video.py")

    # Buscar archivo más reciente en output
    output_dir = os.path.join(SCRIPTS_DIR, "..", "..", "output")
    latest_img = None
    latest_vid = None
    if os.path.exists(output_dir):
        files = sorted(
            [f for f in os.listdir(output_dir) if f.endswith((".png", ".jpg"))],
            key=lambda f: os.path.getmtime(os.path.join(output_dir, f)),
            reverse=True,
        )
        if files:
            latest_img = os.path.join(output_dir, files[0])
        videos = sorted(
            [f for f in os.listdir(output_dir) if f.endswith(".mp4")],
            key=lambda f: os.path.getmtime(os.path.join(output_dir, f)),
            reverse=True,
        )
        if videos:
            latest_vid = os.path.join(output_dir, videos[0])

    # Publicar
    message = random.choice(MESSAGES)
    run_script("post_to_social.py")

    # Guardar log
    log_path = os.path.join(SCRIPTS_DIR, "..", "..", "logs", "scheduler.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(f"[{now}] {message}\n")

    print(f"✅ Ciclo completo. Próximo en {INTERVAL_HOURS} horas.\n")


def main():
    print(f"🚀 BlueWave Scheduler iniciado")
    print(f"⏰ Intervalo: cada {INTERVAL_HOURS} horas")
    print(f"🔴 Presiona Ctrl+C para detener\n")

    while True:
        try:
            generate_and_post()
            time.sleep(INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n🛑 Scheduler detenido por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
