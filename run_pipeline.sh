#!/usr/bin/env bash
set -e

echo "=========================================="
echo "Iniciando Dashboard de Afluencia del Metro"
echo "=========================================="

echo "0. Sincronizando entorno virtual y dependencias..."
uv sync

echo "1. Extrayendo datos de la API..."
uv run python cdmx_api.py

echo "2. Limpiando y transformando datos..."
uv run python clean_data.py

echo "3. Iniciando el Dashboard..."
uv run fastapi dev main.py