#!/usr/bin/env python3
"""
BlueWave - Publicación automática en redes sociales
Template con estructura para cada plataforma.
"""

import os
import json
import webbrowser
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config", "social.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def load_config():
    """Carga o crea la config de redes sociales."""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    config = {
        "twitter": {"enabled": True, "api_key": "", "api_secret": ""},
        "facebook": {"enabled": True, "api_key": "", "api_secret": ""},
        "instagram": {"enabled": True, "api_key": "", "api_secret": ""},
        "youtube": {"enabled": True, "api_key": "", "client_secret": ""},
        "discord": {"enabled": True, "webhook_url": ""},
        "tiktok": {"enabled": True, "api_key": "", "api_secret": ""},
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"📝 Config creada: {CONFIG_PATH}")
    print("Edítala con tus API keys antes de usar.")
    return config


def post_to_twitter(text: str, image_path: str = None):
    print(f"📱 Publicando en Twitter: {text[:50]}...")
    # TODO: Implementar con tweepy
    print("ℹ️ Pendiente: instalar tweepy y configurar API keys")


def post_to_facebook(text: str, image_path: str = None):
    print(f"📱 Publicando en Facebook: {text[:50]}...")
    # TODO: Implementar con facebook-sdk
    print("ℹ️ Pendiente: instalar facebook-sdk y configurar API keys")


def post_to_instagram(image_path: str, caption: str = ""):
    print(f"📱 Publicando en Instagram...")
    # TODO: Instagram Basic Display API
    print("ℹ️ Pendiente: configurar Instagram Basic Display API")


def post_to_youtube(video_path: str, title: str, description: str = ""):
    print(f"📱 Subiendo a YouTube: {title}")
    # TODO: YouTube Data API v3
    print("ℹ️ Pendiente: configurar YouTube Data API")


def send_to_discord(message: str, webhook_url: str = None):
    import requests
    url = webhook_url or ""
    if not url.startswith("http"):
        print("⚠️ Discord webhook no configurado")
        return
    payload = {"content": message}
    try:
        r = requests.post(url, json=payload)
        if r.ok:
            print("✅ Mensaje enviado a Discord")
        else:
            print(f"❌ Error Discord: {r.status_code}")
    except ImportError:
        print("ℹ️ Instala requests: pip install requests")


def post_to_tiktok(video_path: str, description: str = ""):
    print(f"📱 Publicando en TikTok...")
    # TODO: TikTok Business API
    print("ℹ️ Pendiente: configurar TikTok Business API")


def post_all(text: str, image_path: str = None, video_path: str = None):
    """Publica en todas las redes configuradas."""
    config = load_config()

    if config.get("twitter", {}).get("enabled"):
        post_to_twitter(text, image_path)
    if config.get("facebook", {}).get("enabled"):
        post_to_facebook(text, image_path)
    if config.get("instagram", {}).get("enabled") and image_path:
        post_to_instagram(image_path, text)
    if config.get("youtube", {}).get("enabled") and video_path:
        post_to_youtube(video_path, f"BlueWave - {text}", text)
    if config.get("discord", {}).get("enabled"):
        send_to_discord(f"**{text}**\n{image_path or video_path or ''}",
                        config["discord"].get("webhook_url"))
    if config.get("tiktok", {}).get("enabled") and video_path:
        post_to_tiktok(video_path, text)


if __name__ == "__main__":
    load_config()
    print("✅ Script de posting listo. Edita config/social.json con tus API keys.")
