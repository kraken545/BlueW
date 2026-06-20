# Plan de Automatización de Redes Sociales - BlueWave

## Estrategia General

Publicar automáticamente contenido promocional de BlueWave en 6 plataformas usando **n8n auto-hosteado en Oracle Cloud (free tier)**.

## Plataformas a gestionar

1. **Twitter/X** - Contenido corto, memes, actualizaciones
2. **Facebook** - Posts comunitarios, eventos
3. **Instagram** - Fotos, Reels cortos
4. **YouTube** - Videos informativos/tutoriales
5. **Discord** - Anuncios automáticos en canal
6. **TikTok** - Videos virales cortos

---

## Arquitectura del Sistema

```
Oracle Cloud Free Tier (Always Free)
├── Ubuntu Server (4 ARM cores, 24GB RAM)
│   └── n8n (automatización)
│       ├── Nodo: Generar contenido con IA (OpenAI API gratuita o local)
│       ├── Nodo: Crear imágenes con DALL-E / Stable Diffusion
│       ├── Nodo: Publicar en Twitter/X (API)
│       ├── Nodo: Publicar en Facebook (API)
│       ├── Nodo: Publicar en Instagram (API)
│       ├── Nodo: Subir a YouTube (API)
│       ├── Nodo: Enviar a Discord (Webhook)
│       └── Nodo: Publicar en TikTok (API)
```

## Instalación de n8n en Oracle Cloud (Gratis)

### 1. Crear cuenta en Oracle Cloud
- Ve a [oracle.com/cloud/free](https://oracle.com/cloud/free)
- Regístrate con tarjeta de crédito (no te cobrarán si usas solo free tier)
- Crea una instancia "Always Free" con:
  - **Shape:** VM.Standard.A1.Flex (4 OCPU, 24 GB RAM)
  - **OS:** Ubuntu 22.04 o 24.04
  - **Disco:** 200 GB (total free)

### 2. Conectar por SSH
```bash
ssh -i ~/.ssh/tu-llave opc@<IP-de-tu-instancia>
```

### 3. Instalar n8n
```bash
# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs git

# Instalar n8n globalmente
sudo npm install -g n8n

# Crear servicio para que n8n siempre corra
nohup n8n &
```

### 4. Acceder a n8n
- Abre en tu navegador: `http://<IP-de-tu-instancia>:5678`
- Crea cuenta de usuario local
- Listo para crear flujos

## Flujos de Automatización Recomendados

### Flujo 1: Contenido Diario Automático
```
Schedule (cada 6h) → 
  OpenAI → Generar tweet/post sobre Curaçao/BlueWave →
  DALL-E → Generar imagen relacionada →
  Twitter → Publicar tweet con imagen →
  Facebook → Publicar mismo contenido →
  Instagram → Publicar imagen con descripción →
  Discord → Enviar anuncio al canal
```

### Flujo 2: Videos Semanales
```
Schedule (cada semana) →
  Script Python (local con FFmpeg) → 
    - Unir clips de video/imágenes de Curaçao
    - Añadir texto "BlueWave" y música
    - Exportar formato corto (Reels/TikTok) y largo (YouTube) →
  YouTube → Subir video largo →
  TikTok → Publicar video corto →
  Instagram Reels → Publicar video →
  Twitter → Publicar clip de vista previa
```

### Flujo 3: Noticias y Precio
```
Schedule (cada hora) →
  Solana RPC → Consultar precio de BLUEW →
  Comparar cambios →
  Si cambió >5% → 
    Publicar en todas las redes: "BlueWave update: +X% 🚀"
```

## APIs Necesarias

| Plataforma | API | Costo |
|---|---|---|
| Twitter/X | API v2 (Free tier: 1500 tweets/mes) | Gratis |
| Facebook | Graph API | Gratis |
| Instagram | Basic Display API | Gratis |
| YouTube | YouTube Data API v3 | Gratis (10,000 unidades/día) |
| Discord | Webhooks | Gratis |
| TikTok | TikTok Business API | Gratis |

## Script Base para Crear Videos (Python + FFmpeg)

Crear archivo `scripts/generar_video.py`:

```python
import subprocess
import os

# Ejemplo: crear un video simple con imagen + audio
subprocess.run([
    "ffmpeg",
    "-loop", "1",
    "-i", "logo.png",
    "-i", "musica_fondo.mp3",
    "-c:v", "libx264",
    "-t", "15",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "video_promo.mp4"
])
```

## Checklist de Instalación

- [ ] Cuenta Oracle Cloud creada
- [ ] Instancia Always Free creada
- [ ] SSH funcionando
- [ ] n8n instalado y accesible en puerto 5678
- [ ] FFmpeg instalado (`sudo apt install ffmpeg`)
- [ ] Conexión de APIs de redes sociales
- [ ] Flujo de contenido diario funcionando
- [ ] Prueba de publicación en al menos 1 red

---

*Documento parte del proyecto BlueWave (BLUEW) - Curaçao Good Vibes*
