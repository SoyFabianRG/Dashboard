#!/usr/bin/env bash
set -e

echo "========================================"
echo "Iniciando el Pipeline de Datos del Metro"
echo "========================================"

# Verificamos si .venv existe. Si no, lo creamos y preparamos.
if [ ! -d ".venv" ]; then
    echo "0. Creando entorno virtual e instalando dependencias con uv..."
    uv venv
    uv pip install -e .
else
    echo "0. Entorno virtual detectado."
fi

# Al usar 'uv run', no necesitamos hacer 'source' ni 'overlay use'.
# uv se encarga de ejecutar todo dentro del .venv automáticamente.

echo "1. Extrayendo datos de la API (Extract)..."
uv run python cdmx_api.py

echo "2. Limpiando y transformando datos (Transform & Load)..."
uv run python clean_data.py

echo "3. Iniciando el Dashboard (FastAPI)..."
uv run fastapi dev main.py