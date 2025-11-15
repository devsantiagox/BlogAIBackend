#!/bin/bash
# Cambiar al directorio del script
cd "$(dirname "$0")"
echo "Iniciando servidor AI-Blog Backend..."
echo "Directorio: $(pwd)"
echo ""
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

