from typing import List
from src.services.database import db_service
from src.models.fund import Fund, FundResponse
from src.exceptions import FundNotFoundException

class FundService:
    def __init__(self):
        self.table_name = 'funds'
        self._initialize_funds()
    
    def _initialize_funds(self):
        """Inicializo los 5 fondos requeridos"""
        funds_data = [
            {
                "fund_id": "FPV_BTG_PACTUAL_RECAUDADORA",
                "name": "FPV_BTG_PACTUAL_RECAUDADORA",
                "category": "FPV",
                "minimum_amount": 75000,
                "is_active": True
            },
            {
                "fund_id": "FPV_BTG_PACTUAL_ECOPETROL",
                "name": "FPV_BTG_PACTUAL_ECOPETROL",
                "category": "FPV",
                "minimum_amount": 125000,
                "is_active": True
            },
            {
                "fund_id": "DEUDAPRIVADA",
                "name": "DEUDAPRIVADA",
                "category": "FPV",
                "minimum_amount": 50000,
                "is_active": True
            },
            {
                "fund_id": "FDO-ACCIONES",
                "name": "FDO-ACCIONES",
                "category": "FIC",
                "minimum_amount": 250000,
                "is_active": True
            },
            {
                "fund_id": "FPV_BTG_PACTUAL_DINAMICA",
                "name": "FPV_BTG_PACTUAL_DINAMICA",
                "category": "FIC",
                "minimum_amount": 100000,
                "is_active": True
            }
        ]
        
        for fund_data in funds_data:
            existing = db_service.get_item(self.table_name, {"fund_id": fund_data["fund_id"]})
            if not existing:
                db_service.create_item(self.table_name, fund_data)
    
    def get_fund(self, fund_id: str) -> FundResponse:
        """Obtengo fondo por ID"""
        fund_item = db_service.get_item(self.table_name, {"fund_id": fund_id})
        if not fund_item:
            raise FundNotFoundException(fund_id)
        return FundResponse(**fund_item)
    
    def get_all_funds(self) -> List[FundResponse]:
        """Obtengo todos los fondos"""
        funds = db_service.scan_items(self.table_name)
        return [FundResponse(**fund) for fund in funds]
    
    def get_active_funds(self) -> List[FundResponse]:
        """Obtengo solo fondos activos"""
        funds = db_service.scan_items(
            self.table_name,
            "is_active = :is_active",
            {":is_active": True}
        )
        return [FundResponse(**fund) for fund in funds]

# Instancia global del servicio
fund_service = FundService()