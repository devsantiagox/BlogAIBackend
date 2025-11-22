from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from dotenv import load_dotenv

from database import get_db, engine, Base
from models import User, Post
from schemas import (
    UserCreate,
    UserResponse,
    Token,
    PostGenerate,
    PostResponse,
    PostCreate
)
from auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from gemini_service import generate_blog_post
from validators import validate_database_connection, validate_gemini_api, get_health_status

load_dotenv()

# Validar conexiones al iniciar
print("=" * 50)
print("Validando conexiones...")
print("=" * 50)

# Validar base de datos
db_valid, db_message = validate_database_connection(engine)
if db_valid:
    print(f"✓ Base de datos: {db_message}")
    # Crear las tablas solo si la conexión es exitosa
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Tablas de base de datos creadas/verificadas")
    except Exception as e:
        print(f"⚠ Error al crear tablas: {str(e)}")
else:
    print(f"✗ Base de datos: {db_message}")
    print("⚠ La aplicación puede no funcionar correctamente sin conexión a la base de datos")

# Validar Gemini API
gemini_valid, gemini_message = validate_gemini_api()
if gemini_valid:
    print(f"✓ Gemini API: {gemini_message}")
else:
    print(f"✗ Gemini API: {gemini_message}")
    print("⚠ La generación de artículos no funcionará sin la API de Gemini")

print("=" * 50)

app = FastAPI(
    title="AI-Blog API",
    description="API para generar artículos de blog usando IA",
    version="1.0.0"
)

# Configurar CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        # Permitir cualquier subdominio de github.io
        "https://*.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "AI-Blog API",
        "version": "1.0.0",
        "endpoints": {
            "register": "POST /register",
            "login": "POST /token",
            "generate_post": "POST /generate-post (protegido)",
            "get_posts": "GET /posts (público)",
            "health": "GET /health (estado de servicios)"
        }
    }


@app.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de salud de los servicios
    (Base de datos y Gemini API)
    """
    health_status = get_health_status(engine)
    if health_status["status"] == "healthy":
        return health_status
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status
        )


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario
    """
    try:
        # Verificar si el usuario ya existe
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear nuevo usuario
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    except HTTPException:
        # Re-raise HTTP exceptions (como el email duplicado)
        raise
    except Exception as e:
        # Rollback en caso de error
        db.rollback()
        # Log del error para debugging
        import traceback
        error_detail = f"Error al registrar usuario: {str(e)}"
        print(f"ERROR en /register: {error_detail}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )


@app.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login de usuario. Devuelve un token JWT
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/generate-post", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def generate_post(
    post_data: PostGenerate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Genera un artículo de blog usando IA (protegido por JWT)
    """
    try:
        # Generar el artículo usando Gemini
        generated_content = generate_blog_post(post_data.prompt)
        
        # Crear el post en la base de datos
        db_post = Post(
            title=generated_content["title"],
            body=generated_content["body"],
            seo_keywords=generated_content["seo_keywords"],
            author_id=current_user.id
        )
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        
        return db_post
    
    except ValueError as e:
        error_str = str(e)
        # Manejar errores de cuota como 429 (Too Many Requests)
        if "cuota" in error_str.lower() or "quota" in error_str.lower() or "429" in error_str:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_str
            )
        # Otros errores de validación
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_str
        )
    except Exception as e:
        error_str = str(e)
        # Manejar errores de cuota de Gemini
        if "429" in error_str or "quota" in error_str.lower() or "limit" in error_str.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Se ha excedido la cuota de la API de Gemini. Por favor espera un minuto antes de intentar nuevamente. Error: {error_str[:200]}"
            )
        # Otros errores
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el artículo: {error_str}"
        )


@app.get("/posts", response_model=list[PostResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los artículos generados (endpoint público)
    """
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return posts


@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un artículo específico por ID (endpoint público)
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artículo no encontrado"
        )
    return post


@app.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Obtiene información del usuario actual (protegido)
    """
    return current_user


