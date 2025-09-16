from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from src.config import settings
from src.models.user import UserResponse

class JWTHandler:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
    
    def create_access_token(self, user: UserResponse) -> str:
        """Creo token de acceso JWT"""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = {
            "sub": user.user_id,
            "email": user.email,
            "role": user.role,
            "exp": expire
        }
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifico y decodifico token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.PyJWTError:
            return None
    
    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Obtengo información del usuario desde el token"""
        payload = self.verify_token(token)
        if payload:
            return {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role")
            }
        return None

# Instancia global
jwt_handler = JWTHandler()
