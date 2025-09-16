from typing import List, Optional, Dict, Any
from src.services.database import db_service
from src.models.transaction import Transaction, TransactionCreate, TransactionResponse
from src.exceptions import TransactionNotFoundException
from src.utils import generate_id
from boto3.dynamodb.conditions import Key

class TransactionService:
    def __init__(self):
        self.table_name = 'transactions'
    
    def create_transaction(self, transaction_data: TransactionCreate) -> TransactionResponse:
        """Crear nueva transacción"""
        transaction_id = generate_id("txn")
        transaction_item = {
            'transaction_id': transaction_id,
            'user_id': transaction_data.user_id,
            'type': transaction_data.type.value,
            'fund_id': transaction_data.fund_id,
            'amount': transaction_data.amount,
            'balance_before': transaction_data.balance_before,
            'balance_after': transaction_data.balance_after,
            'status': transaction_data.status.value,
            'created_at': generate_id()
        }
        
        # Guardar en DynamoDB
        db_service.create_item(self.table_name, transaction_item)
        
        return TransactionResponse(**transaction_item)
    
    def get_transaction(self, transaction_id: str) -> TransactionResponse:
        """Obtener transacción por ID"""
        transactions = db_service.scan_items(
            self.table_name,
            "transaction_id = :transaction_id",
            {":transaction_id": transaction_id}
        )
        
        if not transactions:
            raise TransactionNotFoundException(transaction_id)
        
        return TransactionResponse(**transactions[0])
    
    def get_user_transactions(self, user_id: str, current_user: dict = None) -> List[TransactionResponse]:
        """Obtengo transacciones - admin ve todas, cliente solo las suyas"""
        if current_user and current_user.get("role") == "admin":
            # Admin ve todas las transacciones
            transactions = db_service.scan_items(self.table_name)
        else:
            # Cliente ve solo las suyas
            transactions = db_service.query_items(
                self.table_name,
                "user_id = :user_id",
                {":user_id": user_id}
            )
        
        # Ordenar por fecha de creación (más recientes primero)
        transactions.sort(key=lambda x: x['created_at'], reverse=True)
        
        return [TransactionResponse(**txn) for txn in transactions]
    
    def get_user_transactions_by_type(self, user_id: str, transaction_type: str) -> List[TransactionResponse]:
        """Obtener transacciones de un usuario por tipo"""
        transactions = db_service.scan_items(
            self.table_name,
            "user_id = :user_id AND #type = :type",
            {
                ":user_id": user_id,
                ":type": transaction_type
            }
        )
        
        # Ordenar por fecha de creación (más recientes primero)
        transactions.sort(key=lambda x: x['created_at'], reverse=True)
        
        return [TransactionResponse(**txn) for txn in transactions]
    
    def get_fund_transactions(self, fund_id: str) -> List[TransactionResponse]:
        """Obtener todas las transacciones de un fondo"""
        transactions = db_service.scan_items(
            self.table_name,
            "fund_id = :fund_id",
            {":fund_id": fund_id}
        )
        
        # Ordenar por fecha de creación (más recientes primero)
        transactions.sort(key=lambda x: x['created_at'], reverse=True)
        
        return [TransactionResponse(**txn) for txn in transactions]
    
    def get_transactions_by_status(self, status: str) -> List[TransactionResponse]:
        """Obtener transacciones por estado"""
        transactions = db_service.scan_items(
            self.table_name,
            "#status = :status",
            {":status": status}
        )
        
        # Ordenar por fecha de creación (más recientes primero)
        transactions.sort(key=lambda x: x['created_at'], reverse=True)
        
        return [TransactionResponse(**txn) for txn in transactions]
    
    def get_all_transactions(self) -> List[TransactionResponse]:
        """Obtener todas las transacciones"""
        transactions = db_service.scan_items(self.table_name)
        
        # Ordenar por fecha de creación (más recientes primero)
        transactions.sort(key=lambda x: x['created_at'], reverse=True)
        
        return [TransactionResponse(**txn) for txn in transactions]

# Instancia global del servicio
transaction_service = TransactionService()