from fastapi import HTTPException
from typing import Optional

class BTGException(Exception):
    """Excepción base para la aplicación BTG Pactual"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InsufficientBalanceException(BTGException):
    """Excepción cuando no hay saldo suficiente"""
    def __init__(self, fund_name: str):
        message = f"No tiene saldo disponible para vincularse al fondo {fund_name}"
        super().__init__(message, 400)

class FundNotFoundException(BTGException):
    """Excepción cuando el fondo no existe"""
    def __init__(self, fund_id: str):
        message = f"Fondo {fund_id} no encontrado"
        super().__init__(message, 404)

class UserNotFoundException(BTGException):
    """Excepción cuando el usuario no existe"""
    def __init__(self, user_id: str):
        message = f"Usuario {user_id} no encontrado"
        super().__init__(message, 404)

class SubscriptionNotFoundException(BTGException):
    """Excepción cuando la suscripción no existe"""
    def __init__(self, subscription_id: str):
        message = f"Suscripción {subscription_id} no encontrada"
        super().__init__(message, 404)

class InvalidAmountException(BTGException):
    """Excepción cuando el monto es inválido"""
    def __init__(self, message: str = "Monto inválido"):
        super().__init__(message, 400)

class FundInactiveException(BTGException):
    """Excepción cuando el fondo está inactivo"""
    def __init__(self, fund_id: str):
        message = f"Fondo {fund_id} está inactivo"
        super().__init__(message, 400)

class DuplicateSubscriptionException(BTGException):
    """Excepción cuando ya existe una suscripción activa"""
    def __init__(self, user_id: str, fund_id: str):
        message = f"Ya existe una suscripción activa para el usuario {user_id} en el fondo {fund_id}"
        super().__init__(message, 400)

class TransactionNotFoundException(BTGException):
    """Excepción cuando la transacción no existe"""
    def __init__(self, transaction_id: str):
        message = f"Transacción {transaction_id} no encontrada"
        super().__init__(message, 404)

class NotificationNotFoundException(BTGException):
    """Excepción cuando la notificación no existe"""
    def __init__(self, notification_id: str):
        message = f"Notificación {notification_id} no encontrada"
        super().__init__(message, 404)

class DuplicateUserException(BTGException):
    """Excepción cuando ya existe un usuario con ese email"""
    def __init__(self, email: str):
        message = f"Ya existe un usuario con el email {email}"
        super().__init__(message, 400)