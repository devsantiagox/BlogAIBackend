# 🧪 Guía para Probar la API en Postman

Esta guía te muestra cómo probar todos los endpoints de la API usando Postman.

## 📋 Configuración Inicial

### Base URL
- **Local**: `http://localhost:8000`
- **Producción**: `https://tu-backend.onrender.com`

---

## 🔐 1. REGISTRO (POST /register)

### Configuración

**Método**: `POST`
**URL**: `http://localhost:8000/register`

**Headers**:
```
Content-Type: application/json
```

**Body** (seleccionar `raw` > `JSON`):
```json
{
  "email": "usuario@example.com",
  "password": "miContrasena123"
}
```

### Ejemplo de Respuesta Exitosa (201 Created)
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "created_at": "2025-11-22T03:00:16.401337Z"
}
```

### Ejemplo de Respuesta de Error (400 Bad Request)
```json
{
  "detail": "El email ya está registrado"
}
```

---

## 🔑 2. LOGIN (POST /token)

### ⚠️ IMPORTANTE: Este endpoint usa `form-data`, NO `JSON`

### Configuración

**Método**: `POST`
**URL**: `http://localhost:8000/token`

**Headers**:
```
Content-Type: application/x-www-form-urlencoded
```

**Body** (seleccionar `x-www-form-urlencoded`):
| Key | Value |
|-----|-------|
| `username` | `usuario@example.com` |
| `password` | `miContrasena123` |
| `grant_type` | `password` *(opcional)* |

### 📝 Nota Importante:
- El campo se llama **`username`** pero debe contener el **email** del usuario
- NO uses `email` como campo, debe ser `username`
- El campo `grant_type` es opcional, pero puedes incluirlo con valor `password`

### Ejemplo de Respuesta Exitosa (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3VhcmlvQGV4YW1wbGUuY29tIiwiZXhwIjoxNjk4MDAwMDAwfQ.xyz123...",
  "token_type": "bearer"
}
```

### Ejemplo de Respuesta de Error (401 Unauthorized)
```json
{
  "detail": "Email o contraseña incorrectos"
}
```

---

## 📝 3. GENERAR ARTÍCULO (POST /generate-post)

### ⚠️ Requiere Autenticación JWT

### Configuración

**Método**: `POST`
**URL**: `http://localhost:8000/generate-post`

**Headers**:
```
Content-Type: application/json
Authorization: Bearer <tu-token-aqui>
```

**Body** (seleccionar `raw` > `JSON`):
```json
{
  "prompt": "Escribe sobre las ventajas de la inteligencia artificial en la educación moderna"
}
```

### Ejemplo de Respuesta Exitosa (201 Created)
```json
{
  "id": 1,
  "title": "Las Ventajas de la Inteligencia Artificial en la Educación Moderna",
  "body": "La inteligencia artificial está transformando...",
  "seo_keywords": "IA, educación, tecnología, aprendizaje",
  "author_id": 1,
  "created_at": "2025-11-22T03:15:30.123456Z",
  "updated_at": null
}
```

---

## 👤 4. OBTENER INFORMACIÓN DEL USUARIO (GET /me)

### ⚠️ Requiere Autenticación JWT

### Configuración

**Método**: `GET`
**URL**: `http://localhost:8000/me`

**Headers**:
```
Authorization: Bearer <tu-token-aqui>
```

**Body**: No requiere body

### Ejemplo de Respuesta Exitosa (200 OK)
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "created_at": "2025-11-22T03:00:16.401337Z"
}
```

---

## 📰 5. OBTENER TODOS LOS ARTÍCULOS (GET /posts)

### Público (NO requiere autenticación)

### Configuración

**Método**: `GET`
**URL**: `http://localhost:8000/posts`

**Query Parameters** (opcionales):
- `skip`: Número de artículos a saltar (default: 0)
- `limit`: Número máximo de artículos a retornar (default: 100)

**Ejemplo**: `http://localhost:8000/posts?skip=0&limit=10`

**Headers**: No requiere headers especiales

### Ejemplo de Respuesta Exitosa (200 OK)
```json
[
  {
    "id": 1,
    "title": "Las Ventajas de la IA en la Educación",
    "body": "La inteligencia artificial está transformando...",
    "seo_keywords": "IA, educación",
    "author_id": 1,
    "created_at": "2025-11-22T03:15:30.123456Z",
    "updated_at": null
  },
  {
    "id": 2,
    "title": "Otro Artículo",
    "body": "Contenido del artículo...",
    "seo_keywords": null,
    "author_id": 1,
    "created_at": "2025-11-22T04:20:45.789012Z",
    "updated_at": null
  }
]
```

---

## 📄 6. OBTENER UN ARTÍCULO ESPECÍFICO (GET /posts/{post_id})

### Público (NO requiere autenticación)

### Configuración

**Método**: `GET`
**URL**: `http://localhost:8000/posts/1`

*(Reemplaza `1` con el ID del artículo)*

**Headers**: No requiere headers especiales

### Ejemplo de Respuesta Exitosa (200 OK)
```json
{
  "id": 1,
  "title": "Las Ventajas de la IA en la Educación",
  "body": "La inteligencia artificial está transformando...",
  "seo_keywords": "IA, educación",
  "author_id": 1,
  "created_at": "2025-11-22T03:15:30.123456Z",
  "updated_at": null
}
```

---

## 🏥 7. HEALTH CHECK (GET /health)

### Público

### Configuración

**Método**: `GET`
**URL**: `http://localhost:8000/health`

**Headers**: No requiere headers especiales

### Ejemplo de Respuesta Exitosa (200 OK)
```json
{
  "status": "healthy",
  "database": {
    "connected": true,
    "message": "Conexión a la base de datos exitosa"
  },
  "gemini_api": {
    "connected": true,
    "message": "Conexión a Gemini API exitosa"
  }
}
```

---

## 🔄 Flujo Completo de Prueba en Postman

### Paso 1: Registrar un Usuario
1. Crea una nueva petición `POST` a `http://localhost:8000/register`
2. Configura el body como `JSON` con email y password
3. Guarda el `id` del usuario creado

### Paso 2: Hacer Login
1. Crea una nueva petición `POST` a `http://localhost:8000/token`
2. **IMPORTANTE**: Usa `x-www-form-urlencoded` en el body
3. Agrega:
   - `username`: el email del usuario
   - `password`: la contraseña
4. Guarda el `access_token` de la respuesta

### Paso 3: Usar el Token
1. En las peticiones protegidas, agrega el header:
   ```
   Authorization: Bearer <tu-token-aqui>
   ```
2. El token expira después de 30 minutos (configurable)

### Paso 4: Generar un Artículo
1. Usa el token del Paso 2
2. Haz una petición `POST` a `http://localhost:8000/generate-post`
3. En el body (JSON), agrega el `prompt`

### Paso 5: Ver los Artículos
1. Haz una petición `GET` a `http://localhost:8000/posts`
2. No requiere autenticación

---

## 💡 Tips para Postman

### 1. Variables de Entorno
Crea un entorno en Postman para facilitar el cambio entre local y producción:

**Variables**:
- `base_url`: `http://localhost:8000` (local) o `https://tu-backend.onrender.com` (producción)
- `token`: Se actualiza automáticamente después del login

**Uso**: `{{base_url}}/register` en lugar de `http://localhost:8000/register`

### 2. Scripts Automáticos
En la petición de **Login**, puedes agregar un script de prueba para guardar automáticamente el token:

**Tests Tab** en Postman:
```javascript
// Guardar el token automáticamente
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.access_token);
    console.log("Token guardado:", jsonData.access_token);
}
```

Luego en las peticiones protegidas, usa:
```
Authorization: Bearer {{token}}
```

### 3. Colección de Peticiones
Crea una colección en Postman con todas estas peticiones para organizarte mejor.

---

## 🐛 Solución de Problemas

### Error 401 Unauthorized en endpoints protegidos
- Verifica que el token esté en el header: `Authorization: Bearer <token>`
- Verifica que el token no haya expirado (30 minutos por defecto)
- Asegúrate de que no haya espacios extra en el header

### Error 400 Bad Request en Login
- Verifica que estés usando `x-www-form-urlencoded` y NO `JSON`
- Verifica que el campo se llame `username` (no `email`)
- Verifica que el email y contraseña sean correctos

### Error 500 Internal Server Error
- Revisa los logs del servidor para ver el error específico
- Verifica que la base de datos esté conectada
- Verifica que todas las variables de entorno estén configuradas

---

## 📚 Recursos Adicionales

- **Swagger UI**: `http://localhost:8000/docs` - Documentación interactiva
- **ReDoc**: `http://localhost:8000/redoc` - Documentación alternativa
- **Health Check**: `http://localhost:8000/health` - Estado de servicios

¡Listo para probar tu API en Postman! 🚀

