from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from datetime import datetime

from src.services.user_service import user_service
from src.services.fund_service import fund_service
from src.services.subscription_service import subscription_service
from src.services.transaction_service import transaction_service
from src.services.notification_service import notification_service

from src.models.user import UserCreate, UserUpdate, UserResponse, UserLogin, TokenResponse, UserRole
from src.models.fund import FundCreate, FundUpdate, FundResponse
from src.models.subscription import SubscriptionCreate, SubscriptionResponse
from src.models.transaction import TransactionCreate, TransactionType, TransactionStatus, TransactionResponse
from src.models.notification import NotificationCreate, NotificationType, NotificationChannel, NotificationStatus, NotificationResponse

from src.exceptions import (
    UserNotFoundException, 
    FundNotFoundException, 
    SubscriptionNotFoundException,
    InsufficientBalanceException,
    DuplicateUserException
)

from src.auth.jwt_handler import jwt_handler
from src.auth.security import get_current_user, get_current_user_full, require_client, require_admin

router = APIRouter()

# ==================== MÉTODOS AUXILIARES ====================

def _validate_subscription_request(subscription_data: SubscriptionCreate) -> tuple[FundResponse, UserResponse]:
    """Verifico que el usuario puede suscribirse al fondo"""
    # Busco el fondo y verifico que esté disponible
    fund = fund_service.get_fund(subscription_data.fund_id)
    if not fund.is_active:
        raise HTTPException(status_code=400, detail=f"El fondo {fund.name} no está disponible en este momento")
    
    # Verifico que el monto cumple con el mínimo requerido
    if subscription_data.amount < fund.minimum_amount:
        error_message = f"Para suscribirse al fondo {fund.name} necesita mínimo COP ${fund.minimum_amount:,.0f}. Usted tiene COP ${subscription_data.amount:,.0f}"
        raise HTTPException(status_code=400, detail=error_message)
    
    # Verifico que el usuario tiene suficiente saldo
    user = user_service.get_user(subscription_data.user_id)
    if user.balance < subscription_data.amount:
        raise HTTPException(
            status_code=400,
            detail=f"No tiene saldo disponible para vincularse al fondo {fund.name}"
        )
    
    return fund, user

def _create_subscription_transaction(user: UserResponse, fund: FundResponse, amount: float, 
                                   saldo_anterior: float, saldo_nuevo: float, 
                                   tipo_transaccion: TransactionType) -> None:
    """Registro la transacción en el historial del usuario"""
    transaction_data = TransactionCreate(
        user_id=user.user_id,
        type=tipo_transaccion,
        fund_id=fund.fund_id,
        amount=amount,
        balance_before=saldo_anterior,
        balance_after=saldo_nuevo,
        status=TransactionStatus.COMPLETED
    )
    transaction_service.create_transaction(transaction_data)

def _create_subscription_notification(user: UserResponse, fund: FundResponse, amount: float, 
                                    tipo_notificacion: NotificationType, accion: str) -> None:
    """Envío notificación al usuario sobre su operación"""
    canal = NotificationChannel.EMAIL if user.notification_preference == "email" else NotificationChannel.SMS
    mensaje = f"Su suscripción al fondo {fund.name} {accion} por COP ${amount:,.0f} ha sido exitosa"
    
    notification_data = NotificationCreate(
        user_id=user.user_id,
        type=tipo_notificacion,
        channel=canal,
        content=mensaje,
        status=NotificationStatus.PENDING
    )
    notification_service.create_notification(notification_data)

# ==================== AUTENTICACIÓN ====================

@router.post("/auth/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    """Inicio sesión y obtengo token JWT"""
    user = user_service.authenticate_user(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    access_token = jwt_handler.create_access_token(user)
    return TokenResponse(access_token=access_token, user=user)

@router.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Registro nuevo cliente y obtengo token JWT"""
    try:
        # Solo se pueden registrar clientes por este endpoint
        user = user_service.create_user(user_data, role=UserRole.CLIENT)
        access_token = jwt_handler.create_access_token(user)
        return TokenResponse(access_token=access_token, user=user)
    except (DuplicateUserException, ValueError) as e:
        raise HTTPException(status_code=400, detail=e.message if hasattr(e, 'message') else str(e))

# ==================== USUARIOS ====================

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """Creo nuevo cliente"""
    try:
        # Solo se pueden crear clientes por este endpoint
        return user_service.create_user(user_data, role=UserRole.CLIENT)
    except (DuplicateUserException, ValueError) as e:
        raise HTTPException(status_code=400, detail=e.message if hasattr(e, 'message') else str(e))

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Obtengo usuario por ID"""
    try:
        return user_service.get_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

@router.get("/users", response_model=List[UserResponse])
async def get_all_users():
    """Obtengo todos los usuarios"""
    return user_service.get_all_users()

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_data: UserUpdate):
    """Actualizo usuario"""
    try:
        return user_service.update_user(user_id, user_data)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

# ==================== FONDOS ====================

@router.post("/funds", response_model=FundResponse, status_code=status.HTTP_201_CREATED)
async def create_fund(fund_data: FundCreate):
    """Creo nuevo fondo"""
    try:
        return fund_service.create_fund(fund_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/funds", response_model=List[FundResponse])
async def get_all_funds():
    """Obtengo todos los fondos"""
    return fund_service.get_all_funds()

@router.get("/funds/active", response_model=List[FundResponse])
async def get_active_funds():
    """Obtengo solo fondos activos"""
    return fund_service.get_active_funds()

@router.get("/funds/{fund_id}", response_model=FundResponse)
async def get_fund(fund_id: str):
    """Obtengo fondo por ID"""
    try:
        return fund_service.get_fund(fund_id)
    except FundNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

@router.put("/funds/{fund_id}", response_model=FundResponse)
async def update_fund(fund_id: str, fund_data: FundUpdate):
    """Actualizo fondo"""
    try:
        return fund_service.update_fund(fund_id, fund_data)
    except FundNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

# ==================== SUSCRIPCIONES ====================

@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(subscription_data: SubscriptionCreate, current_user: dict = Depends(require_client)):
    """Suscribo al usuario a un fondo de inversión"""
    try:
        # Verifico que todo esté en orden para la suscripción
        fund, user = _validate_subscription_request(subscription_data)
        
        # Creo la nueva suscripción
        subscription = subscription_service.create_subscription(subscription_data)
        
        # Actualizo el saldo del usuario
        nuevo_saldo = user.balance - subscription_data.amount
        user_service.update_balance(subscription_data.user_id, nuevo_saldo)
        
        # Registro la transacción y envío notificación
        _create_subscription_transaction(user, fund, subscription_data.amount, user.balance, nuevo_saldo, TransactionType.SUBSCRIPTION)
        _create_subscription_notification(user, fund, subscription_data.amount, NotificationType.SUBSCRIPTION_CONFIRMATION, "por")
        
        return subscription
        
    except HTTPException:
        raise
    except (UserNotFoundException, FundNotFoundException) as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subscriptions/user/{user_id}", response_model=List[SubscriptionResponse])
async def get_user_subscriptions(user_id: str, current_user: dict = Depends(get_current_user)):
    """Muestro solo las suscripciones activas del usuario"""
    return subscription_service.get_active_user_subscriptions(user_id, current_user)

@router.get("/subscriptions/user/{user_id}/active", response_model=List[SubscriptionResponse])
async def get_active_user_subscriptions(user_id: str, current_user: dict = Depends(get_current_user)):
    """Muestro solo las suscripciones activas del usuario"""
    return subscription_service.get_active_user_subscriptions(user_id, current_user)

@router.delete("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def cancel_subscription(subscription_id: str, current_user: dict = Depends(require_client)):
    """Cancelo la suscripción del usuario y le devuelvo su dinero"""
    try:
        # Busco la suscripción que quiere cancelar
        subscription = subscription_service.get_subscription(subscription_id)
        user = user_service.get_user(subscription.user_id)
        fund = fund_service.get_fund(subscription.fund_id)
        
        # Procedo a cancelar la suscripción
        cancelled_subscription = subscription_service.cancel_subscription(subscription_id)
        
        # Le devuelvo el dinero al usuario
        nuevo_saldo = user.balance + subscription.amount
        user_service.update_balance(subscription.user_id, nuevo_saldo)
        
        # Registro la operación y envío notificación
        _create_subscription_transaction(user, fund, subscription.amount, user.balance, nuevo_saldo, TransactionType.CANCELLATION)
        _create_subscription_notification(user, fund, subscription.amount, NotificationType.CANCELLATION_CONFIRMATION, "ha sido cancelada. Se ha devuelto")
        
        return cancelled_subscription
        
    except SubscriptionNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== TRANSACCIONES ====================

@router.get("/transactions/user/{user_id}", response_model=List[TransactionResponse])
async def get_user_transactions(user_id: str, current_user: dict = Depends(get_current_user)):
    """Muestro el historial completo de transacciones del usuario"""
    return transaction_service.get_user_transactions(user_id, current_user)

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str, current_user: dict = Depends(require_client)):
    """Obtengo transacción por ID"""
    return transaction_service.get_transaction(transaction_id)

# ==================== NOTIFICACIONES ====================

@router.get("/notifications/user/{user_id}", response_model=List[NotificationResponse])
async def get_user_notifications(user_id: str, current_user: dict = Depends(get_current_user)):
    """Muestro todas las notificaciones del usuario"""
    return notification_service.get_user_notifications(user_id, current_user)

@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: str, current_user: dict = Depends(require_client)):
    """Obtengo notificación por ID"""
    return notification_service.get_notification(notification_id)