"""
Pruebas para módulo de suscripciones
"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.services.subscription_service import subscription_service

class TestSubscriptionService:
    """Pruebas para SubscriptionService"""
    
    @patch('src.services.subscription_service.db_service')
    def test_create_subscription_success(self, mock_db_service, mock_subscription):
        """Creo suscripción exitosamente"""
        mock_db_service.create_item.return_value = mock_subscription.model_dump()
        
        from src.models.subscription import SubscriptionCreate
        subscription_data = SubscriptionCreate(
            user_id="user_test_123",
            fund_id="FPV_BTG_PACTUAL_RECAUDADORA",
            amount=100000
        )
        
        result = subscription_service.create_subscription(subscription_data)
        
        assert result.subscription_id is not None
        assert result.status == "active"
    
    @patch('src.services.subscription_service.db_service')
    def test_cancel_subscription_success(self, mock_db_service, mock_subscription):
        """Cancelo suscripción exitosamente"""
        # Mock para la suscripción original (activa) - primera llamada a get_subscription
        original_subscription = mock_subscription.model_dump()
        
        # Mock para la suscripción cancelada (después de update) - segunda llamada a get_subscription
        cancelled_subscription = mock_subscription.model_dump()
        cancelled_subscription["status"] = "cancelled"
        cancelled_subscription["cancelled_at"] = "2025-01-01T12:00:00"
        
        # Configurar el mock para que scan_items retorne diferentes valores en cada llamada
        mock_db_service.scan_items.side_effect = [
            [original_subscription],  # Primera llamada (antes de cancelar)
            [cancelled_subscription]  # Segunda llamada (después de cancelar)
        ]
        
        result = subscription_service.cancel_subscription("sub_test_123")
        
        assert result.status == "cancelled"

class TestSubscriptionEndpoints:
    """Pruebas para endpoints de suscripciones"""
    
    @patch('src.api.routes.user_service')
    @patch('src.api.routes.fund_service')
    @patch('src.api.routes.subscription_service')
    @patch('src.api.routes.transaction_service')
    @patch('src.api.routes.notification_service')
    @patch('src.auth.jwt_handler.JWTHandler.verify_token')
    def test_create_subscription_success(self, mock_verify_token, mock_notification_service, mock_transaction_service, 
                                       mock_subscription_service, mock_fund_service, mock_user_service, 
                                       client, mock_user, mock_fund, mock_subscription, auth_headers):
        """Creo suscripción exitosamente"""
        # "Quemamos" el payload del JWT
        mock_verify_token.return_value = {
            "sub": "user_test_123",
            "email": "test@example.com",
            "role": "client"
        }
        mock_fund_service.get_fund.return_value = mock_fund
        mock_user_service.get_user.return_value = mock_user
        mock_subscription_service.create_subscription.return_value = mock_subscription
        mock_user_service.update_balance.return_value = mock_user
        
        subscription_data = {
            "user_id": "user_test_123",
            "fund_id": "FPV_BTG_PACTUAL_RECAUDADORA",
            "amount": 100000
        }
        
        response = client.post("/api/v1/subscriptions", json=subscription_data, headers=auth_headers)
        
        assert response.status_code == 201
        assert "subscription_id" in response.json()
    
    @patch('src.api.routes.user_service')
    @patch('src.api.routes.fund_service')
    @patch('src.auth.jwt_handler.JWTHandler.verify_token')
    def test_create_subscription_insufficient_amount(self, mock_verify_token, mock_fund_service, mock_user_service, 
                                                   client, mock_user, mock_fund, auth_headers):
        """Error cuando monto es menor al mínimo"""
        # "Quemamos" el payload del JWT
        mock_verify_token.return_value = {
            "sub": "user_test_123",
            "email": "test@example.com",
            "role": "client"
        }
        mock_fund_service.get_fund.return_value = mock_fund
        mock_user_service.get_user.return_value = mock_user
        
        subscription_data = {
            "user_id": "user_test_123",
            "fund_id": "FPV_BTG_PACTUAL_RECAUDADORA",
            "amount": 50000  # Menor al mínimo de 75000
        }
        
        response = client.post("/api/v1/subscriptions", json=subscription_data, headers=auth_headers)
        
        assert response.status_code == 400
        assert "necesita mínimo" in response.json()["detail"]
    
    @patch('src.api.routes.subscription_service')
    @patch('src.api.routes.user_service')
    @patch('src.api.routes.fund_service')
    @patch('src.api.routes.transaction_service')
    @patch('src.api.routes.notification_service')
    @patch('src.auth.jwt_handler.JWTHandler.verify_token')
    def test_cancel_subscription_success(self, mock_verify_token, mock_notification_service, mock_transaction_service,
                                       mock_fund_service, mock_user_service, mock_subscription_service,
                                       client, mock_user, mock_fund, mock_subscription, auth_headers):
        """Cancelo suscripción exitosamente"""
        # "Quemamos" el payload del JWT
        mock_verify_token.return_value = {
            "sub": "user_test_123",
            "email": "test@example.com",
            "role": "client"
        }
        mock_subscription_service.get_subscription.return_value = mock_subscription
        mock_user_service.get_user.return_value = mock_user
        mock_fund_service.get_fund.return_value = mock_fund
        # Mock para la suscripción cancelada
        cancelled_subscription = mock_subscription.model_dump()
        cancelled_subscription["status"] = "cancelled"
        mock_subscription_service.cancel_subscription.return_value = cancelled_subscription
        mock_user_service.update_balance.return_value = mock_user
        
        response = client.delete("/api/v1/subscriptions/sub_test_123", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"
    
    def test_create_subscription_unauthorized(self, client):
        """Error cuando no hay autorización"""
        subscription_data = {
            "user_id": "user_test_123",
            "fund_id": "FPV_BTG_PACTUAL_RECAUDADORA",
            "amount": 100000
        }
        
        response = client.post("/api/v1/subscriptions", json=subscription_data)
        
        assert response.status_code == 403
