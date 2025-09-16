"""
Pruebas para módulo de fondos
"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.services.fund_service import fund_service

class TestFundService:
    """Pruebas para FundService"""
    
    @patch('src.services.fund_service.db_service')
    def test_get_fund_success(self, mock_db_service, mock_fund):
        """Obtengo fondo exitosamente"""
        mock_db_service.get_item.return_value = mock_fund.model_dump()
        
        result = fund_service.get_fund("FPV_BTG_PACTUAL_RECAUDADORA")
        
        assert result.fund_id == "FPV_BTG_PACTUAL_RECAUDADORA"
        assert result.minimum_amount == 75000.0
    
    @patch('src.services.fund_service.db_service')
    def test_get_fund_not_found(self, mock_db_service):
        """Error cuando fondo no existe"""
        mock_db_service.get_item.return_value = None
        
        from src.exceptions import FundNotFoundException
        with pytest.raises(FundNotFoundException):
            fund_service.get_fund("FONDO_INEXISTENTE")
    
    @patch('src.services.fund_service.db_service')
    def test_get_active_funds(self, mock_db_service, mock_fund):
        """Obtengo solo fondos activos"""
        mock_db_service.scan_items.return_value = [mock_fund.model_dump()]
        
        result = fund_service.get_active_funds()
        
        assert len(result) == 1
        assert result[0].is_active == True

class TestFundEndpoints:
    """Pruebas para endpoints de fondos"""
    
    def test_get_all_funds(self, client):
        """Obtengo todos los fondos"""
        response = client.get("/api/v1/funds")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_active_funds(self, client):
        """Obtengo fondos activos"""
        response = client.get("/api/v1/funds/active")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
