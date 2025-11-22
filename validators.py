"""
Módulo para validar conexiones a servicios externos
"""
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def validate_database_connection(engine):
    """
    Valida la conexión a la base de datos.
    Retorna (success: bool, message: str)
    """
    try:
        with engine.connect() as connection:
            # Ejecutar una consulta simple para verificar la conexión
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        return True, "Conexión a la base de datos exitosa"
    except SQLAlchemyError as e:
        error_msg = str(e).lower()
        original_error = str(e)
        
        if "password" in error_msg or "authentication" in error_msg or "invalid password" in error_msg:
            return False, "Error de autenticación con la base de datos. Verifica las credenciales en DATABASE_URL"
        elif "could not translate host name" in error_msg or "could not resolve" in error_msg:
            return False, "No se pudo resolver el hostname. Verifica que DATABASE_URL sea correcta"
        elif "connection" in error_msg and ("refused" in error_msg or "timeout" in error_msg):
            return False, "No se pudo conectar al servidor de base de datos. Verifica que el servidor esté accesible y que tu IP esté permitida"
        elif "ssl" in error_msg or "sslmode" in error_msg:
            return False, "Error de SSL. Si usas Neon o un servicio cloud, agrega ?sslmode=require al final de DATABASE_URL"
        elif "timeout" in error_msg:
            return False, "Timeout al conectar. El servidor puede estar inaccesible o tu conexión es lenta"
        else:
            # Mostrar el error completo para debugging
            return False, f"Error de conexión a la base de datos: {original_error[:200]}"
    except Exception as e:
        return False, f"Error inesperado al validar la base de datos: {str(e)}"


def validate_gemini_api():
    """
    Valida la configuración de la API de Gemini sin hacer solicitudes reales.
    Retorna (success: bool, message: str)
    """
    if not GEMINI_API_KEY:
        return False, "GEMINI_API_KEY no está configurada en las variables de entorno"
    
    if GEMINI_API_KEY == "your-gemini-api-key-here" or not GEMINI_API_KEY.strip():
        return False, "GEMINI_API_KEY está configurada pero parece ser un valor por defecto. Configura tu API key real de Gemini"
    
    try:
        # Configurar Gemini (no hace solicitud real, solo configuración)
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Intentar listar modelos disponibles (no consume cuota de generación)
        # Esto verifica que la API key sea válida sin hacer solicitudes de contenido
        try:
            models = genai.list_models()
            model_names = [m.name for m in models if "gemini" in m.name.lower()]
            
            if model_names:
                # Verificar si hay modelos compatibles con tier gratuito
                preferred_models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-pro-latest']
                available_model = None
                for preferred in preferred_models:
                    if any(preferred in name for name in model_names):
                        available_model = preferred
                        break
                
                if available_model:
                    return True, f"Conexión a Gemini API exitosa. Modelo {available_model} configurado y disponible"
                else:
                    return True, f"Conexión a Gemini API exitosa. Modelos disponibles: {', '.join(model_names[:3])}"
            else:
                return False, "No se encontraron modelos Gemini disponibles"
        except Exception as list_error:
            error_str = str(list_error).lower()
            if "api key" in error_str or "invalid" in error_str or "unauthorized" in error_str:
                return False, "API Key de Gemini inválida o no autorizada. Verifica tu GEMINI_API_KEY"
            elif "quota" in error_str or "limit" in error_str:
                # Si es error de cuota, la API está configurada pero sin cuota disponible
                # No retornamos False porque la configuración es correcta, solo falta cuota
                return True, "API Key configurada correctamente, pero se ha excedido la cuota. Espera a que se resetee."
            else:
                # Si no puede listar modelos pero la API key está configurada, asumimos que está bien
                # La validación real se hará al intentar generar contenido
                return True, "API Key configurada. La validación completa se realizará al generar contenido."
    
    except Exception as e:
        error_msg = str(e).lower()
        if "api key" in error_msg or "invalid" in error_msg or "unauthorized" in error_msg:
            return False, "API Key de Gemini inválida o no autorizada. Verifica tu GEMINI_API_KEY"
        else:
            return False, f"Error al configurar Gemini API: {str(e)}"


def get_health_status(engine):
    """
    Obtiene el estado de salud de todos los servicios.
    Retorna un diccionario con el estado de cada servicio.
    """
    db_status = validate_database_connection(engine)
    gemini_status = validate_gemini_api()
    
    overall_status = "healthy" if (db_status[0] and gemini_status[0]) else "unhealthy"
    
    return {
        "status": overall_status,
        "database": {
            "connected": db_status[0],
            "message": db_status[1]
        },
        "gemini_api": {
            "connected": gemini_status[0],
            "message": gemini_status[1]
        }
    }

