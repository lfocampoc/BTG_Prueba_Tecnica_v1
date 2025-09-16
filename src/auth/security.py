from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from src.auth.jwt_handler import jwt_handler
from src.services.user_service import user_service

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Obtengo usuario actual desde token JWT"""
    token = credentials.credentials
    user_data = jwt_handler.get_user_from_token(token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_data

async def get_current_user_full(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Obtengo usuario completo desde base de datos"""
    user_data = await get_current_user(credentials)
    user = user_service.get_user(user_data["user_id"])
    return user

def require_role(required_role: str):
    """Decorator para requerir rol específico"""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
        return current_user
    return role_checker

# Dependencias comunes
require_client = require_role("client")
require_admin = require_role("admin")
