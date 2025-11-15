"""
Script para probar las conexiones a la base de datos y Gemini API
"""
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar validadores
from database import engine
from validators import validate_database_connection, validate_gemini_api, get_health_status

def test_connections():
    """Prueba las conexiones y muestra los resultados"""
    print("=" * 60)
    print("PRUEBA DE CONEXIONES - AI-Blog Backend")
    print("=" * 60)
    print()
    
    # Verificar variables de entorno
    print("📋 Verificando variables de entorno...")
    db_url = os.getenv("DATABASE_URL")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if db_url:
        # Ocultar la contraseña en la URL para seguridad
        if "@" in db_url:
            parts = db_url.split("@")
            if ":" in parts[0]:
                user_pass = parts[0].split("://")[1] if "://" in parts[0] else parts[0]
                if ":" in user_pass:
                    user = user_pass.split(":")[0]
                    db_url_display = db_url.replace(user_pass, f"{user}:***")
                else:
                    db_url_display = db_url
            else:
                db_url_display = db_url
        else:
            db_url_display = db_url
        print(f"  ✓ DATABASE_URL: {db_url_display[:50]}...")
    else:
        print("  ✗ DATABASE_URL: No configurada")
    
    if gemini_key:
        # Mostrar solo los primeros y últimos caracteres
        if len(gemini_key) > 10:
            masked_key = f"{gemini_key[:4]}...{gemini_key[-4:]}"
        else:
            masked_key = "***"
        print(f"  ✓ GEMINI_API_KEY: {masked_key}")
    else:
        print("  ✗ GEMINI_API_KEY: No configurada")
    
    print()
    print("-" * 60)
    print()
    
    # Probar conexión a base de datos
    print("🗄️  Probando conexión a Base de Datos...")
    try:
        db_valid, db_message = validate_database_connection(engine)
        if db_valid:
            print(f"  ✅ {db_message}")
        else:
            print(f"  ❌ {db_message}")
            # Mostrar sugerencias si es un error de conexión
            if "No se pudo conectar" in db_message or "could not translate" in db_message.lower():
                print()
                print("  💡 Sugerencias:")
                print("     - Verifica que DATABASE_URL sea correcta")
                print("     - Si usas Neon/Cloud, verifica que la IP esté permitida")
                print("     - Prueba agregar ?sslmode=require al final de DATABASE_URL")
    except Exception as e:
        print(f"  ❌ Error al validar: {str(e)}")
    print()
    
    # Probar conexión a Gemini API
    print("🤖 Probando conexión a Gemini API...")
    gemini_valid, gemini_message = validate_gemini_api()
    if gemini_valid:
        print(f"  ✅ {gemini_message}")
    else:
        print(f"  ❌ {gemini_message}")
    print()
    
    print("-" * 60)
    print()
    
    # Resumen
    print("📊 RESUMEN:")
    print()
    health_status = get_health_status(engine)
    
    status_icon = "✅" if health_status["status"] == "healthy" else "❌"
    print(f"  Estado General: {status_icon} {health_status['status'].upper()}")
    print()
    print(f"  Base de Datos: {'✅ Conectada' if health_status['database']['connected'] else '❌ Desconectada'}")
    print(f"  Gemini API: {'✅ Conectada' if health_status['gemini_api']['connected'] else '❌ Desconectada'}")
    print()
    
    if health_status["status"] == "healthy":
        print("🎉 ¡Todas las conexiones están funcionando correctamente!")
        return 0
    else:
        print("⚠️  Hay problemas con algunas conexiones. Revisa los mensajes arriba.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = test_connections()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

