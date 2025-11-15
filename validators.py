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
    Valida la conexión y configuración de la API de Gemini.
    Retorna (success: bool, message: str)
    """
    if not GEMINI_API_KEY:
        return False, "GEMINI_API_KEY no está configurada en las variables de entorno"
    
    if GEMINI_API_KEY == "your-gemini-api-key-here" or not GEMINI_API_KEY.strip():
        return False, "GEMINI_API_KEY está configurada pero parece ser un valor por defecto. Configura tu API key real de Gemini"
    
    try:
        # Configurar Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Intentar crear un modelo para verificar la conexión
        # Esto es más directo que listar todos los modelos
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            # Hacer una prueba simple con un prompt muy corto
            test_response = model.generate_content("test", generation_config={"max_output_tokens": 1})
            return True, "Conexión a Gemini API exitosa. Modelo gemini-2.0-flash-exp disponible"
        except Exception as model_error:
            # Si el modelo específico falla, intentar con otro modelo común
            try:
                model = genai.GenerativeModel('gemini-pro')
                test_response = model.generate_content("test", generation_config={"max_output_tokens": 1})
                return True, "Conexión a Gemini API exitosa. Usando modelo gemini-pro (gemini-2.0-flash-exp no disponible)"
            except:
                # Si ambos fallan, verificar si es un problema de API key o de modelo
                error_str = str(model_error).lower()
                if "api key" in error_str or "invalid" in error_str or "unauthorized" in error_str:
                    raise ValueError("API Key inválida")
                else:
                    # Intentar listar modelos como último recurso
                    try:
                        models = genai.list_models()
                        model_names = [m.name for m in models if "gemini" in m.name.lower()]
                        if model_names:
                            return True, f"Conexión a Gemini API exitosa. Modelos disponibles: {', '.join(model_names[:3])}"
                        else:
                            return False, f"Error al acceder a modelos Gemini: {str(model_error)}"
                    except:
                        return False, f"Error al conectar con Gemini API: {str(model_error)}"
    
    except Exception as e:
        error_msg = str(e).lower()
        if "api key" in error_msg or "invalid" in error_msg or "unauthorized" in error_msg:
            return False, "API Key de Gemini inválida o no autorizada. Verifica tu GEMINI_API_KEY"
        elif "quota" in error_msg or "limit" in error_msg:
            return False, "Se ha excedido la cuota de la API de Gemini. Verifica tu plan y límites"
        else:
            return False, f"Error al conectar con Gemini API: {str(e)}"


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

