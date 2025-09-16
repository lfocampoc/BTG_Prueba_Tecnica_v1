"""
Pruebas para módulo de notificaciones
"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.services.notification_service import notification_service

class TestNotificationService:
    """Pruebas para NotificationService"""
    
    @patch('src.services.notification_service.db_service')
    def test_create_notification_success(self, mock_db_service):
        """Creo notificación exitosamente"""
        mock_db_service.create_item.return_value = {}
        
        from src.models.notification import NotificationCreate, NotificationType, NotificationChannel, NotificationStatus
        notification_data = NotificationCreate(
            user_id="user_test_123",
            type=NotificationType.SUBSCRIPTION_CONFIRMATION,
            channel=NotificationChannel.EMAIL,
            content="Test notification",
            status=NotificationStatus.PENDING
        )
        
        result = notification_service.create_notification(notification_data)
        
        assert result.user_id == "user_test_123"
        assert result.type == "subscription_confirmation"
    
    @patch('src.services.notification_service.db_service')
    def test_get_user_notifications(self, mock_db_service):
        """Obtengo notificaciones de usuario"""
        mock_notifications = [
            {
                "notification_id": "notif_1",
                "user_id": "user_test_123",
                "type": "subscription_confirmation",
                "channel": "email",
                "content": "Test notification",
                "status": "pending",
                "created_at": "2025-01-01T00:00:00",
                "sent_at": None
            }
        ]
        mock_db_service.query_items.return_value = mock_notifications
        
        result = notification_service.get_user_notifications("user_test_123")
        
        assert len(result) == 1
        assert result[0].user_id == "user_test_123"

class TestNotificationEndpoints:
    """Pruebas para endpoints de notificaciones"""
    
    @patch('src.api.routes.notification_service')
    @patch('src.auth.jwt_handler.JWTHandler.verify_token')
    def test_get_user_notifications(self, mock_verify_token, mock_notification_service, client, auth_headers, mock_user):
        """Obtengo notificaciones de usuario"""
        # "Quemamos" el payload del JWT
        mock_verify_token.return_value = {
            "sub": "user_test_123",
            "email": "test@example.com",
            "role": "client"
        }
        mock_notification_service.get_user_notifications.return_value = []
        
        response = client.get("/api/v1/notifications/user/user_test_123", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_user_notifications_unauthorized(self, client):
        """Error cuando no hay autorización"""
        response = client.get("/api/v1/notifications/user/user_test_123")
        
        assert response.status_code == 403
