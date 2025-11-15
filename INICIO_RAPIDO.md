# 🚀 Inicio Rápido - AI-Blog Backend

## Iniciar el Servidor

### Opción 1: Usando Python directamente (Recomendado)
```bash
python -m uvicorn main:app --reload
```

### Opción 2: Usando el script de inicio
**Windows:**
```bash
start_server.bat
```

**Linux/Mac:**
```bash
chmod +x start_server.sh
./start_server.sh
```

## Verificar que el servidor está corriendo

Una vez iniciado, deberías ver algo como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
==================================================
Validando conexiones...
==================================================
✓ Base de datos: ...
✓ Gemini API: ...
==================================================
INFO:     Application startup complete.
```

## Acceder a la API

- **API Principal**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Verificar Estado de Conexiones

### Desde el navegador:
Abre: http://localhost:8000/health

### Desde la terminal:
```bash
curl http://localhost:8000/health
```

### Usando el script de prueba:
```bash
python test_connections.py
```

## Solución de Problemas

### "uvicorn no se reconoce"
Usa: `python -m uvicorn main:app --reload`

### "ModuleNotFoundError"
Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Puerto 8000 ocupado
Usa otro puerto:
```bash
python -m uvicorn main:app --reload --port 8001
```

## Notas

- El servidor se recarga automáticamente cuando cambias archivos (--reload)
- Las validaciones de conexión se muestran al iniciar
- El endpoint `/health` te permite verificar el estado en tiempo real

