"""
Pruebas para módulo de transacciones
"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.services.transaction_service import transaction_service

class TestTransactionService:
    """Pruebas para TransactionService"""
    
    @patch('src.services.transaction_service.db_service')
    def test_create_transaction_success(self, mock_db_service):
        """Creo transacción exitosamente"""
        mock_db_service.create_item.return_value = {}
        
        from src.models.transaction import TransactionCreate, TransactionType, TransactionStatus
        transaction_data = TransactionCreate(
            user_id="user_test_123",
            type=TransactionType.SUBSCRIPTION,
            fund_id="FPV_BTG_PACTUAL_RECAUDADORA",
            amount=100000,
            balance_before=500000,
            balance_after=400000,
            status=TransactionStatus.COMPLETED
        )
        
        result = transaction_service.create_transaction(transaction_data)
        
        assert result.user_id == "user_test_123"
        assert result.type == "subscription"
    
    @patch('src.services.transaction_service.db_service')
    def test_get_user_transactions(self, mock_db_service):
        """Obtengo transacciones de usuario"""
        mock_transactions = [
            {
                "transaction_id": "txn_1",
                "user_id": "user_test_123",
                "type": "subscription",
                "fund_id": "FPV_BTG_PACTUAL_RECAUDADORA",
                "amount": 100000,
                "balance_before": 500000,
                "balance_after": 400000,
                "status": "completed",
                "created_at": "2025-01-01T00:00:00"
            }
        ]
        mock_db_service.query_items.return_value = mock_transactions
        
        result = transaction_service.get_user_transactions("user_test_123")
        
        assert len(result) == 1
        assert result[0].user_id == "user_test_123"

class TestTransactionEndpoints:
    """Pruebas para endpoints de transacciones"""
    
    @patch('src.api.routes.transaction_service')
    @patch('src.auth.jwt_handler.JWTHandler.verify_token')
    def test_get_user_transactions(self, mock_verify_token, mock_transaction_service, client, auth_headers, mock_user):
        """Obtengo transacciones de usuario"""
        # "Quemamos" el payload del JWT
        mock_verify_token.return_value = {
            "sub": "user_test_123",
            "email": "test@example.com",
            "role": "client"
        }
        mock_transaction_service.get_user_transactions.return_value = []
        
        response = client.get("/api/v1/transactions/user/user_test_123", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_user_transactions_unauthorized(self, client):
        """Error cuando no hay autorización"""
        response = client.get("/api/v1/transactions/user/user_test_123")
        
        assert response.status_code == 403
