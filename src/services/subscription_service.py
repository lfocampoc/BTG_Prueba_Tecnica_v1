from typing import List, Optional, Dict, Any
from src.services.database import db_service
from src.models.subscription import Subscription, SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from src.exceptions import SubscriptionNotFoundException, DuplicateSubscriptionException, InsufficientBalanceException
from src.utils import generate_id, get_current_timestamp
from boto3.dynamodb.conditions import Key

class SubscriptionService:
    def __init__(self):
        self.table_name = 'subscriptions'
    
    def create_subscription(self, subscription_data: SubscriptionCreate) -> SubscriptionResponse:
        """Creo nueva suscripción"""
        # Creo suscripción
        subscription_id = generate_id("sub")
        current_time = get_current_timestamp()
        subscription_item = {
            'subscription_id': subscription_id,
            'user_id': subscription_data.user_id,
            'fund_id': subscription_data.fund_id,
            'amount': subscription_data.amount,
            'status': 'active',
            'created_at': current_time,
            'cancelled_at': None
        }
        
        # Guardo en DynamoDB
        db_service.create_item(self.table_name, subscription_item)
        
        return SubscriptionResponse(**subscription_item)
    
    def get_subscription(self, subscription_id: str) -> SubscriptionResponse:
        """Obtengo suscripción por ID"""
        subscriptions = db_service.scan_items(
            self.table_name,
            "subscription_id = :subscription_id",
            {":subscription_id": subscription_id}
        )
        
        if not subscriptions:
            raise SubscriptionNotFoundException(subscription_id)
        
        return SubscriptionResponse(**subscriptions[0])
    
    def get_active_subscription(self, user_id: str, fund_id: str) -> Optional[SubscriptionResponse]:
        """Obtengo suscripción activa de un usuario a un fondo"""
        subscriptions = db_service.scan_items(
            self.table_name,
            "user_id = :user_id AND fund_id = :fund_id AND #status = :status",
            {
                ":user_id": user_id,
                ":fund_id": fund_id,
                ":status": "active"
            },
            {
                "#status": "status"
            }
        )
        
        if not subscriptions:
            return None
        
        return SubscriptionResponse(**subscriptions[0])
    
    def get_user_subscriptions(self, user_id: str, current_user: dict = None) -> List[SubscriptionResponse]:
        """Obtengo suscripciones - admin ve todas, cliente solo las suyas"""
        if current_user and current_user.get("role") == "admin":
            # Admin ve todas las suscripciones
            subscriptions = db_service.scan_items(self.table_name)
        else:
            # Cliente ve solo las suyas
            subscriptions = db_service.query_items(
                self.table_name,
                "user_id = :user_id",
                {":user_id": user_id}
            )
        
        return [SubscriptionResponse(**sub) for sub in subscriptions]
    
    def get_active_user_subscriptions(self, user_id: str, current_user: dict = None) -> List[SubscriptionResponse]:
        """Obtengo suscripciones activas - admin ve todas, cliente solo las suyas"""
        if current_user and current_user.get("role") == "admin":
            # Admin ve todas las suscripciones activas
            subscriptions = db_service.scan_items(
                self.table_name,
                "#status = :status",
                {":status": "active"},
                {"#status": "status"}
            )
        else:
            # Cliente ve solo las suyas activas
            subscriptions = db_service.scan_items(
                self.table_name,
                "user_id = :user_id AND #status = :status",
                {
                    ":user_id": user_id,
                    ":status": "active"
                },
                {"#status": "status"}
            )
        
        return [SubscriptionResponse(**sub) for sub in subscriptions]
    
    def cancel_subscription(self, subscription_id: str) -> SubscriptionResponse:
        """Cancelo suscripción"""
        subscription = self.get_subscription(subscription_id)
        
        if subscription.status == "cancelled":
            raise SubscriptionNotFoundException(f"Suscripción {subscription_id} ya está cancelada")
        
        # Actualizo estado
        db_service.update_item(
            self.table_name,
            {'subscription_id': subscription_id},
            "SET #status = :status, cancelled_at = :cancelled_at",
            {
                ":status": "cancelled",
                ":cancelled_at": get_current_timestamp()
            },
            {"#status": "status"}
        )
        
        # Retorno suscripción actualizada
        return self.get_subscription(subscription_id)
    
    def get_fund_subscriptions(self, fund_id: str) -> List[SubscriptionResponse]:
        """Obtengo todas las suscripciones de un fondo"""
        subscriptions = db_service.scan_items(
            self.table_name,
            "fund_id = :fund_id",
            {":fund_id": fund_id}
        )
        
        return [SubscriptionResponse(**sub) for sub in subscriptions]
    
    def get_active_fund_subscriptions(self, fund_id: str) -> List[SubscriptionResponse]:
        """Obtengo suscripciones activas de un fondo"""
        subscriptions = db_service.scan_items(
            self.table_name,
            "fund_id = :fund_id AND #status = :status",
            {
                ":fund_id": fund_id,
                ":status": "active"
            },
            {"#status": "status"}
        )
        
        return [SubscriptionResponse(**sub) for sub in subscriptions]

# Instancia global del servicio
subscription_service = SubscriptionService()