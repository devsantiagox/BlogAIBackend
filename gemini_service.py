import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

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

    model = genai.GenerativeModel('gemini-2.0-flash-exp')

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
        raise Exception(f"Error al generar el artículo con Gemini: {str(e)}")


