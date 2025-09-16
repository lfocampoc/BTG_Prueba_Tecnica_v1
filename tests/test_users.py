"""
Pruebas para módulo de usuarios
"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.models.user import UserCreate, UserRole, NotificationPreference
from src.exceptions import UserNotFoundException, DuplicateUserException
from src.services.user_service import user_service

class TestUserService:
    """Pruebas para UserService"""
    
    @patch('src.services.user_service.db_service')
    def test_create_user_client(self, mock_db_service):
        """Creo usuario cliente con saldo inicial"""
        mock_db_service.scan_items.return_value = []
        mock_db_service.create_item.return_value = {}
        
        user_data = UserCreate(
            email="test@example.com",
            phone="+573001234567",
            password="123456",
            notification_preference=NotificationPreference.EMAIL
        )
        
        result = user_service.create_user(user_data, UserRole.CLIENT)
        
        assert result.balance == 500000.0
        assert result.role == "client"
    
    @patch('src.services.user_service.db_service')
    def test_create_user_admin(self, mock_db_service):
        """Creo usuario admin sin saldo inicial"""
        mock_db_service.scan_items.return_value = []
        mock_db_service.create_item.return_value = {}
        
        user_data = UserCreate(
            email="admin@example.com",
            phone="+573001234567",
            password="123456",
            notification_preference=NotificationPreference.EMAIL
        )
        
        result = user_service.create_user(user_data, UserRole.ADMIN)
        
        assert result.balance == 0.0
        assert result.role == "admin"
    
    @patch('src.services.user_service.db_service')
    def test_authenticate_user(self, mock_db_service, mock_user):
        """Autentico usuario correctamente"""
        # Mock del usuario con contraseña hasheada
        user_data = mock_user.model_dump()
        user_data['password'] = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'  # SHA256 de "123456"
        mock_db_service.scan_items.return_value = [user_data]
        
        from src.models.user import UserLogin
        login_data = UserLogin(email="test@example.com", password="123456")
        
        result = user_service.authenticate_user(login_data)
        
        assert result is not None
        assert result.email == "test@example.com"

class TestUserEndpoints:
    """Pruebas para endpoints de usuarios"""
    
    @patch('src.api.routes.user_service')
    def test_register_success(self, mock_user_service, client, mock_user):
        """Registro exitoso de usuario"""
        mock_user_service.create_user.return_value = mock_user
        
        user_data = {
            "email": "test@example.com",
            "phone": "+573001234567",
            "password": "123456",
            "notification_preference": "email"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        assert "access_token" in response.json()
    
    @patch('src.api.routes.user_service')
    def test_login_success(self, mock_user_service, client, mock_user):
        """Login exitoso"""
        mock_user_service.authenticate_user.return_value = mock_user
        
        login_data = {
            "email": "test@example.com",
            "password": "123456"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    @patch('src.api.routes.user_service')
    def test_login_invalid_credentials(self, mock_user_service, client):
        """Login con credenciales inválidas"""
        mock_user_service.authenticate_user.return_value = None
        
        login_data = {
            "email": "test@example.com",
            "password": "wrong_password"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
