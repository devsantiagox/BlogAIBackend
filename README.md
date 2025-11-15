# AI-Blog Backend

Backend para la plataforma de generación de artículos de blog usando IA (Gemini).

## Características

- ✅ Autenticación JWT
- ✅ Registro e inicio de sesión de usuarios
- ✅ Generación de artículos completos usando Gemini AI
- ✅ API pública para consultar artículos
- ✅ Base de datos PostgreSQL
- ✅ CORS configurado para GitHub Pages

## Requisitos

- Python 3.9+
- PostgreSQL (Render proporciona una instancia gratuita)
- API Key de Google Gemini

## Instalación Local

1. Clona el repositorio
```bash
git clone <tu-repo>
cd ProyectoFinalBack
```

2. Crea un entorno virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instala las dependencias
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno
Crea un archivo `.env` basado en `.env.example`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=tu-clave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=tu-api-key-de-gemini
FRONTEND_URL=https://tuusuario.github.io
```

5. Ejecuta las migraciones (crea las tablas)
```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

6. Inicia el servidor
```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## Despliegue en Render

### 1. Preparar la base de datos PostgreSQL

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Crea un nuevo servicio PostgreSQL (Free tier)
3. Copia la "Internal Database URL" o "External Database URL"

### 2. Configurar variables de entorno en Render

En tu servicio Web Service de Render, configura estas variables:

- `DATABASE_URL`: La URL de tu base de datos PostgreSQL de Render
- `SECRET_KEY`: Una clave secreta aleatoria (puedes generar una con: `openssl rand -hex 32`)
- `ALGORITHM`: `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
- `GEMINI_API_KEY`: Tu API key de Google Gemini
- `FRONTEND_URL`: La URL de tu GitHub Pages (ej: `https://tuusuario.github.io`)

### 3. Configurar el servicio Web

1. Crea un nuevo "Web Service" en Render
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3

### 4. Notas importantes

- Render asigna un puerto dinámico, por eso usamos `$PORT` en el start command
- Las tablas se crean automáticamente al iniciar (ver `main.py`)
- Asegúrate de que el servicio PostgreSQL esté en la misma región que tu Web Service

## Endpoints de la API

### Públicos

- `GET /` - Información de la API
- `GET /posts` - Obtener todos los artículos (público)
- `GET /posts/{post_id}` - Obtener un artículo específico

### Autenticación

- `POST /register` - Registro de nuevo usuario
  ```json
  {
    "email": "usuario@example.com",
    "password": "contraseña123"
  }
  ```

- `POST /token` - Login (devuelve JWT)
  ```
  Form data:
  username: usuario@example.com
  password: contraseña123
  ```

### Protegidos (requieren JWT)

- `POST /generate-post` - Generar nuevo artículo
  ```json
  {
    "prompt": "Escribe sobre las ventajas de la inteligencia artificial"
  }
  ```
  Header: `Authorization: Bearer <token>`

- `GET /me` - Información del usuario actual

## Documentación

Una vez que el servidor esté corriendo, puedes acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estructura del Proyecto

```
ProyectoFinalBack/
├── main.py              # Aplicación FastAPI principal
├── database.py          # Configuración de base de datos
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Schemas Pydantic
├── auth.py              # Lógica de autenticación JWT
├── gemini_service.py    # Integración con Gemini API
├── requirements.txt     # Dependencias
├── .env.example         # Ejemplo de variables de entorno
└── README.md           # Este archivo
```

## Obtener API Key de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva API Key
4. Cópiala y úsala en tu variable de entorno `GEMINI_API_KEY`

## Notas de Desarrollo

- El modelo de Gemini usado es `gemini-2.0-flash-exp` (puedes cambiarlo en `gemini_service.py`)
- Las contraseñas se hashean con bcrypt
- Los tokens JWT expiran en 30 minutos por defecto
- CORS está configurado para permitir peticiones desde GitHub Pages

