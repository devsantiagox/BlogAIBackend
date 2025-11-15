# Validaciones de Conexiones

Este documento explica cómo funcionan las validaciones de conexión implementadas en el backend.

## Validaciones Implementadas

### 1. Validación de Base de Datos

La validación de la base de datos se ejecuta:
- **Al iniciar la aplicación**: Se muestra en la consola si la conexión es exitosa o no
- **En el endpoint `/health`**: Permite verificar el estado en tiempo real

**Qué valida:**
- Conexión a PostgreSQL
- Autenticación correcta
- Accesibilidad del servidor

**Mensajes de error comunes:**
- `Error de autenticación`: Credenciales incorrectas en `DATABASE_URL`
- `No se pudo conectar`: El servidor no es accesible o la URL es incorrecta

### 2. Validación de Gemini API

La validación de Gemini API se ejecuta:
- **Al iniciar la aplicación**: Se muestra en la consola si la API está disponible
- **Antes de generar un artículo**: Se valida antes de procesar cada request
- **En el endpoint `/health`**: Permite verificar el estado en tiempo real

**Qué valida:**
- Presencia de `GEMINI_API_KEY` en variables de entorno
- Validez de la API key
- Disponibilidad del modelo `gemini-2.0-flash-exp`
- Conexión exitosa con la API

**Mensajes de error comunes:**
- `GEMINI_API_KEY no está configurada`: Falta la variable de entorno
- `API Key inválida`: La clave no es válida o ha expirado
- `Se ha excedido la cuota`: Límite de uso alcanzado

## Endpoint de Health Check

### GET `/health`

Retorna el estado de salud de todos los servicios:

**Respuesta exitosa (200):**
```json
{
  "status": "healthy",
  "database": {
    "connected": true,
    "message": "Conexión a la base de datos exitosa"
  },
  "gemini_api": {
    "connected": true,
    "message": "Conexión a Gemini API exitosa. Modelo gemini-2.0-flash-exp disponible"
  }
}
```

**Respuesta con errores (503):**
```json
{
  "status": "unhealthy",
  "database": {
    "connected": false,
    "message": "Error de autenticación con la base de datos..."
  },
  "gemini_api": {
    "connected": false,
    "message": "GEMINI_API_KEY no está configurada..."
  }
}
```

## Uso

### Verificar estado al iniciar

Al ejecutar `uvicorn main:app`, verás en la consola:

```
==================================================
Validando conexiones...
==================================================
✓ Base de datos: Conexión a la base de datos exitosa
✓ Tablas de base de datos creadas/verificadas
✓ Gemini API: Conexión a Gemini API exitosa. Modelo gemini-2.0-flash-exp disponible
==================================================
```

O si hay errores:

```
==================================================
Validando conexiones...
==================================================
✗ Base de datos: Error de autenticación con la base de datos...
⚠ La aplicación puede no funcionar correctamente sin conexión a la base de datos
✗ Gemini API: GEMINI_API_KEY no está configurada...
⚠ La generación de artículos no funcionará sin la API de Gemini
==================================================
```

### Verificar estado vía API

```bash
# Verificar estado de salud
curl http://localhost:8000/health

# O desde el navegador
http://localhost:8000/health
```

## Configuración Requerida

Asegúrate de tener estas variables en tu `.env`:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
GEMINI_API_KEY=tu-api-key-real-de-gemini
```

## Notas

- Las validaciones no bloquean el inicio de la aplicación, solo muestran advertencias
- El endpoint `/generate-post` validará Gemini API antes de procesar cada request
- Si la base de datos falla, los endpoints que la requieren fallarán con errores descriptivos
- Si Gemini API falla, el endpoint `/generate-post` retornará un error 503 con detalles

