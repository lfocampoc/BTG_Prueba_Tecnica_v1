"""
Configuración global para pytest
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.api.main import app
from src.models.user import UserResponse, UserRole, NotificationPreference
from src.models.fund import FundResponse
from src.models.subscription import SubscriptionResponse

@pytest.fixture
def client():
    """Cliente de prueba para FastAPI"""
    return TestClient(app)

@pytest.fixture
def mock_user():
    """Usuario mock para pruebas"""
    return UserResponse(
        user_id="user_test_123",
        email="test@example.com",
        phone="+573001234567",
        balance=500000.0,
        notification_preference=NotificationPreference.EMAIL,
        role=UserRole.CLIENT,
        created_at="2025-01-01T00:00:00",
        updated_at="2025-01-01T00:00:00"
    )

@pytest.fixture
def mock_fund():
    """Fondo mock para pruebas"""
    return FundResponse(
        fund_id="FPV_BTG_PACTUAL_RECAUDADORA",
        name="FPV_BTG_PACTUAL_RECAUDADORA",
        category="FPV",
        minimum_amount=75000.0,
        is_active=True,
        created_at="2025-01-01T00:00:00"
    )

@pytest.fixture
def mock_subscription():
    """Suscripción mock para pruebas"""
    return SubscriptionResponse(
        subscription_id="sub_test_123",
        user_id="user_test_123",
        fund_id="FPV_BTG_PACTUAL_RECAUDADORA",
        amount=100000.0,
        status="active",
        created_at="2025-01-01T00:00:00",
        cancelled_at=None
    )

@pytest.fixture
def auth_headers():
    """Headers de autenticación para pruebas"""
    return {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX3Rlc3RfMTIzIiwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIiwicm9sZSI6ImNsaWVudCIsImV4cCI6MTc1Nzk2ODk1MX0.8yX306qp38TzEuKdcjDFXbxxexEiMX-_3mHvUxTvBtk"}

@pytest.fixture(autouse=True)
def mock_jwt_auth():
    """Mock global para JWT - se aplica automáticamente a todos los tests"""
    with patch('src.auth.jwt_handler.JWTHandler.verify_token') as mock_verify_token:
        mock_verify_token.return_value = {
            "sub": "user_test_123",
            "email": "test@example.com",
            "role": "client"
        }
        yield mock_verify_token
