from typing import List, Optional, Dict, Any
from src.services.database import db_service
from src.models.notification import Notification, NotificationCreate, NotificationResponse
from src.exceptions import NotificationNotFoundException
from src.utils import generate_id
from boto3.dynamodb.conditions import Key

class NotificationService:
    def __init__(self):
        self.table_name = 'notifications'
    
    def create_notification(self, notification_data: NotificationCreate) -> NotificationResponse:
        """Crear nueva notificación"""
        notification_id = generate_id("notif")
        notification_item = {
            'notification_id': notification_id,
            'user_id': notification_data.user_id,
            'type': notification_data.type.value,
            'channel': notification_data.channel.value,
            'status': notification_data.status.value,
            'content': notification_data.content,
            'created_at': generate_id(),
            'sent_at': None
        }
        
        # Guardar en DynamoDB
        db_service.create_item(self.table_name, notification_item)
        
        return NotificationResponse(**notification_item)
    
    def get_notification(self, notification_id: str) -> NotificationResponse:
        """Obtener notificación por ID"""
        notifications = db_service.scan_items(
            self.table_name,
            "notification_id = :notification_id",
            {":notification_id": notification_id}
        )
        
        if not notifications:
            raise NotificationNotFoundException(notification_id)
        
        return NotificationResponse(**notifications[0])
    
    def get_user_notifications(self, user_id: str, current_user: dict = None) -> List[NotificationResponse]:
        """Obtengo notificaciones - admin ve todas, cliente solo las suyas"""
        if current_user and current_user.get("role") == "admin":
            # Admin ve todas las notificaciones
            notifications = db_service.scan_items(self.table_name)
        else:
            # Cliente ve solo las suyas usando el índice user_id-index
            notifications = db_service.query_items(
                self.table_name,
                "user_id = :user_id",
                {":user_id": user_id},
                index_name="user_id-index"
            )
        
        # Ordenar por fecha de creación (más recientes primero)
        notifications.sort(key=lambda x: x['created_at'], reverse=True)
        
        return [NotificationResponse(**notif) for notif in notifications]
    
    def get_user_notifications_by_type(self, user_id: str, notification_type: str) -> List[NotificationResponse]:
        """Obtener notificaciones de un usuario por tipo"""
        notifications = db_service.scan_items(
            self.table_name,
            "user_id = :user_id AND #type = :type",
            {
                ":user_id": user_id,
                ":type": notification_type
            },
            {
                "#type": "type"
            }
        )
        
        # Ordenar por fecha de creación (más recientes primero)
        notifications.sort(key=lambda x: x['created_at'], reverse=True)
        
        return [NotificationResponse(**notif) for notif in notifications]
    
    def get_notifications_by_status(self, status: str) -> List[NotificationResponse]:
        """Obtener notificaciones por estado"""
        notifications = db_service.scan_items(
            self.table_name,
            "#status = :status",
            {":status": status}
        )
        
        # Ordenar por fecha de creación (más recientes primero)
        notifications.sort(key=lambda x: x['created_at'], reverse=True)
        
        return [NotificationResponse(**notif) for notif in notifications]
    
    def mark_notification_sent(self, notification_id: str) -> NotificationResponse:
        """Marcar notificación como enviada"""
        notification = self.get_notification(notification_id)
        
        # Actualizar estado
        db_service.update_item(
            self.table_name,
            {'user_id': notification.user_id, 'notification_id': notification_id},
            "SET #status = :status, sent_at = :sent_at",
            {
                ":status": "sent",
                ":sent_at": generate_id()
            }
        )
        
        # Retornar notificación actualizada
        return self.get_notification(notification_id)
    
    def mark_notification_failed(self, notification_id: str) -> NotificationResponse:
        """Marcar notificación como fallida"""
        notification = self.get_notification(notification_id)
        
        # Actualizar estado
        db_service.update_item(
            self.table_name,
            {'user_id': notification.user_id, 'notification_id': notification_id},
            "SET #status = :status",
            {":status": "failed"}
        )
        
        # Retornar notificación actualizada
        return self.get_notification(notification_id)
    
    def get_pending_notifications(self) -> List[NotificationResponse]:
        """Obtener notificaciones pendientes"""
        return self.get_notifications_by_status("pending")
    
    def get_sent_notifications(self) -> List[NotificationResponse]:
        """Obtener notificaciones enviadas"""
        return self.get_notifications_by_status("sent")
    
    def get_failed_notifications(self) -> List[NotificationResponse]:
        """Obtener notificaciones fallidas"""
        return self.get_notifications_by_status("failed")

# Instancia global del servicio
notification_service = NotificationService()