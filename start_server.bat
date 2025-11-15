@echo off
cd /d "%~dp0"
echo Iniciando servidor AI-Blog Backend...
echo Directorio: %CD%
echo.
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause

