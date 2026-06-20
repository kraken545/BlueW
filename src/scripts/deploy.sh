#!/usr/bin/env bash
set -euo pipefail

# ============================================
# BlueWave - Script de despliegue automatizado
# ============================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
info() { echo -e "${BLUE}[i]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; }

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BlueWave - Deploy Automatizado         ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1. Verificar dependencias
info "Verificando dependencias..."

check_dep() {
    if ! command -v "$1" &>/dev/null; then
        err "$1 no instalado. Instala: $2"
        return 1
    fi
    log "$1 encontrado"
}

check_dep "node"  "https://nodejs.org"
check_dep "npm"   "nodejs"
check_dep "python3" "python3"
check_dep "pip3"  "python3-pip"
check_dep "git"   "git"

# 2. Instalar dependencias Python
info "Instalando dependencias Python..."
pip3 install -r "$PROJECT_DIR/requirements.txt" --quiet 2>/dev/null && log "Dependencias Python instaladas" || warn "Error instalando dependencias"

# 3. Instalar dependencias npm si existe package.json
if [ -f "$PROJECT_DIR/package.json" ]; then
    info "Instalando dependencias npm..."
    cd "$PROJECT_DIR"
    npm install --silent 2>/dev/null && log "Dependencias npm instaladas" || warn "Error npm install"
fi

# 4. Verificar Phantom wallet (crear si no existe)
SOLANA_CONFIG="${SOLANA_HOME:-$HOME/.config/solana/id.json}"
if [ ! -f "$SOLANA_CONFIG" ]; then
    warn "No se encontró wallet de Solana en $SOLANA_CONFIG"
    warn "Crea una con: solana-keygen new --outfile ~/.config/solana/id.json"
    warn "O instala Phantom y exporta la private key."
fi

# 5. Verificar estructura de directorios
info "Verificando estructura..."
for dir in assets output logs config; do
    mkdir -p "$PROJECT_DIR/$dir"
done
log "Estructura de directorios OK"

# 6. Crear config por defecto
if [ ! -f "$PROJECT_DIR/config/social.json" ]; then
    python3 "$SCRIPT_DIR/post_to_social.py" 2>/dev/null || true
fi

# 7. Generar primer contenido
info "Generando contenido inicial..."
python3 "$SCRIPT_DIR/generate_content.py" 2>/dev/null && log "Imagen promocional generada" || warn "Error generando imagen"

echo ""
log "Despliegue completado!"
info "Próximos pasos:"
info "  1. Edita config/social.json con tus API keys"
info "  2. Ejecuta: python3 src/scripts/scheduler.py"
info "  3. Para n8n: cd src/docker && docker compose up -d"
echo ""
