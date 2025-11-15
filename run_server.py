#!/usr/bin/env python
"""
Script simple para iniciar el servidor con validaciones
"""
import uvicorn
import sys
import os

# Cambiar al directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Agregar el directorio actual al path de Python
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

if __name__ == "__main__":
    print("=" * 60)
    print("Iniciando AI-Blog Backend Server")
    print("=" * 60)
    print(f"Directorio de trabajo: {os.getcwd()}")
    print()
    print("Servidor disponible en: http://localhost:8000")
    print("Documentación: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print()
    print("Presiona CTRL+C para detener el servidor")
    print("=" * 60)
    print()
    
    try:
        # Verificar que main.py existe
        if not os.path.exists("main.py"):
            print("ERROR: No se encuentra main.py en el directorio actual")
            print(f"Directorio actual: {os.getcwd()}")
            sys.exit(1)
        
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError al iniciar el servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

