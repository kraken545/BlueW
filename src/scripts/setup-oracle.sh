#!/usr/bin/env bash
set -euo pipefail

# =============================================
# BlueWave - Setup Oracle Cloud Free Tier
# Ejecutar DESPUÉS de crear la instancia
# =============================================

echo ""
echo "========================================"
echo "  BlueWave - Setup Oracle Cloud"
echo "========================================"
echo ""

# 1. Sistema actualizado
echo "[1/6] Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Dependencias base
echo "[2/6] Instalando dependencias..."
sudo apt install -y \
    curl git python3 python3-pip \
    ffmpeg \
    docker.io docker-compose-v2 \
    nodejs npm

# 3. n8n global
echo "[3/6] Instalando n8n..."
sudo npm install -g n8n

# 4. Clonar proyecto
echo "[4/6] Clonando proyecto BlueWave..."
if [ ! -d "$HOME/memecoin" ]; then
    git clone https://github.com/TU_USER/TU_REPO.git "$HOME/memecoin" || {
        echo "⚠️ No se pudo clonar. Crea el repo en GitHub primero."
        mkdir -p "$HOME/memecoin"
    }
fi

# 5. Dependencias Python
echo "[5/6] Instalando dependencias Python..."
pip3 install Pillow requests --quiet

# 6. Docker n8n
echo "[6/6] Configurando Docker n8n..."
if [ -f "$HOME/memecoin/src/docker/docker-compose.yml" ]; then
    cd "$HOME/memecoin/src/docker"
    sudo docker compose up -d
    echo "✅ n8n corriendo en http://localhost:5678"
else
    echo "⚠️ docker-compose.yml no encontrado. Iniciando n8n manual..."
    nohup n8n > "$HOME/n8n.log" 2>&1 &
    echo "✅ n8n corriendo en http://localhost:5678"
fi

echo ""
echo "========================================"
echo "  Setup completado!"
echo ""
echo "  n8n:  http://localhost:5678"
echo "  Docs: $HOME/memecoin/docs/"
echo "========================================"
