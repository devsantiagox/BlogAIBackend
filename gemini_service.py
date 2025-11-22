import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re
import time

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def generate_blog_post(prompt: str) -> dict:
    """
    Genera un artículo de blog completo usando Gemini API.
    Retorna un diccionario con: title, body, seo_keywords
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY no está configurada")

    # Usar modelo disponible - gemini-2.5-flash es el modelo flash más reciente disponible
    # Intentar con modelos en orden de preferencia
    models_to_try = [
        'gemini-2.5-flash',      # Modelo flash más reciente (preferido)
        'gemini-2.0-flash',      # Modelo flash alternativo
        'gemini-pro-latest'      # Fallback
    ]
    
    model = None
    model_name = None
    last_error = None
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # Verificar que el modelo funciona intentando usarlo (sin generar contenido todavía)
            # Solo verificamos que se puede instanciar, no generamos contenido
            break
        except Exception as e:
            last_error = str(e)
            continue
    
    if model is None:
        raise ValueError(
            f"No se pudo cargar ningún modelo de Gemini disponible. "
            f"Modelos intentados: {', '.join(models_to_try)}. "
            f"Último error: {last_error}"
        )

    system_prompt = """Eres un experto escritor de blogs. Genera un artículo de blog completo basado en el prompt proporcionado.

El artículo debe incluir:
1. Un título atractivo y descriptivo
2. Un cuerpo de artículo bien estructurado con párrafos, subtítulos si es necesario, y contenido de calidad
3. Palabras clave SEO relevantes separadas por comas

Responde SOLO con un JSON válido en el siguiente formato:
{
    "title": "Título del artículo",
    "body": "Cuerpo completo del artículo con párrafos bien formateados...",
    "seo_keywords": "palabra1, palabra2, palabra3, palabra4, palabra5"
}

No incluyas ningún texto adicional fuera del JSON."""

    full_prompt = f"{system_prompt}\n\nPrompt del usuario: {prompt}"

    try:
        response = model.generate_content(full_prompt)
        
        # Extraer el JSON de la respuesta
        response_text = response.text.strip()
        
        # Limpiar el texto si tiene markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        # Parsear el JSON
        try:
            blog_data = json.loads(response_text)
        except json.JSONDecodeError:
            # Si falla, intentar extraer JSON con regex
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
            if json_match:
                blog_data = json.loads(json_match.group())
            else:
                raise ValueError("No se pudo extraer JSON de la respuesta")
        
        # Validar que tenga los campos necesarios
        if "title" not in blog_data or "body" not in blog_data:
            raise ValueError("La respuesta de Gemini no contiene los campos requeridos")
        
        # Asegurar que seo_keywords existe
        if "seo_keywords" not in blog_data:
            blog_data["seo_keywords"] = ""
        
        return {
            "title": blog_data["title"],
            "body": blog_data["body"],
            "seo_keywords": blog_data.get("seo_keywords", "")
        }
    
    except Exception as e:
        error_str = str(e)
        # Manejar errores de cuota específicamente
        if "429" in error_str or "quota" in error_str.lower() or "limit" in error_str.lower():
            raise ValueError(
                "Se ha excedido la cuota de la API de Gemini. "
                "Por favor, verifica tu plan y límites en https://ai.dev/usage. "
                "El tier gratuito tiene límites de uso por minuto. "
                f"Error: {error_str[:200]}"
            )
        # Otros errores
        raise Exception(f"Error al generar el artículo con Gemini: {error_str}")


