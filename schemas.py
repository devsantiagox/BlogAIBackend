from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Schemas para Usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# Schemas para Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Schemas para Posts
class PostGenerate(BaseModel):
    prompt: str


class PostResponse(BaseModel):
    id: int
    title: str
    body: str
    seo_keywords: Optional[str]
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    body: str
    seo_keywords: Optional[str] = None


