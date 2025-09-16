from typing import Optional, List
from src.services.database import db_service
from src.models.user import UserCreate, UserUpdate, UserResponse, UserLogin, UserRole
from src.exceptions import UserNotFoundException, InsufficientBalanceException, DuplicateUserException
from src.utils import generate_id, get_current_timestamp, format_phone_number, validate_phone_number
from src.config import settings
import hashlib

class UserService:
    def __init__(self):
        self.table_name = 'users'
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Obtengo usuario por email"""
        users = db_service.scan_items(
            self.table_name,
            "email = :email",
            {":email": email}
        )
        
        if not users:
            return None
        
        return UserResponse(**users[0])
    
    def _hash_password(self, password: str) -> str:
        """Encripto contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, user_data: UserCreate, role: UserRole = UserRole.CLIENT) -> UserResponse:
        """Creo nuevo usuario - solo clientes por registro público"""
        if not validate_phone_number(user_data.phone):
            raise ValueError("Número telefónico inválido")
        
        # Verifico que no existe un usuario con ese email
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise DuplicateUserException(user_data.email)
        
        user_id = generate_id("user")
        current_time = get_current_timestamp()
        
        # Solo clientes tienen saldo inicial
        initial_balance = settings.initial_balance if role == UserRole.CLIENT else 0.0
        
        user_item = {
            'user_id': user_id,
            'email': user_data.email,
            'phone': format_phone_number(user_data.phone),
            'password': self._hash_password(user_data.password),
            'balance': initial_balance,
            'notification_preference': user_data.notification_preference.value,
            'role': role.value,
            'created_at': current_time,
            'updated_at': current_time
        }
        
        db_service.create_item(self.table_name, user_item)
        return UserResponse(**user_item)
    
    def authenticate_user(self, login_data: UserLogin) -> Optional[UserResponse]:
        """Autentico usuario con email y contraseña"""
        # Busco por email directamente en la tabla
        users = db_service.scan_items(
            self.table_name,
            "email = :email",
            {":email": login_data.email}
        )
        
        if not users:
            return None
        
        user_item = users[0]  # Tomo el primer resultado
        hashed_password = self._hash_password(login_data.password)
        if user_item.get('password') != hashed_password:
            return None
        
        return UserResponse(**user_item)
    
    def get_user(self, user_id: str) -> UserResponse:
        """Obtengo usuario por ID"""
        users = db_service.scan_items(
            self.table_name,
            "user_id = :user_id",
            {":user_id": user_id}
        )
        if not users:
            raise UserNotFoundException(user_id)
        return UserResponse(**users[0])
    
    def update_balance(self, user_id: str, new_balance: float) -> UserResponse:
        """Actualizo el saldo del usuario"""
        if new_balance < 0:
            raise InsufficientBalanceException("El saldo no puede ser negativo")
        
        print(f"🔍 DEBUG: Actualizando balance para user_id: {user_id}, new_balance: {new_balance}")
        
        # Busco el usuario primero
        users = db_service.scan_items(
            self.table_name,
            "user_id = :user_id",
            {":user_id": user_id}
        )
        
        if not users:
            raise UserNotFoundException(user_id)
        
        user_item = users[0]
        print(f"🔍 DEBUG: Usuario encontrado: {user_item}")
        
        # Actualizo el balance en el item
        user_item['balance'] = new_balance
        user_item['updated_at'] = get_current_timestamp()
        
        # Guardo el item completo usando put_item
        try:
            db_service.create_item(self.table_name, user_item)
            print(f"✅ DEBUG: Balance actualizado exitosamente")
        except Exception as e:
            print(f"❌ DEBUG: Error al actualizar balance: {e}")
            raise
        
        return self.get_user(user_id)
    
    def get_all_users(self) -> List[UserResponse]:
        """Obtengo todos los usuarios"""
        users = db_service.scan_items(self.table_name)
        return [UserResponse(**user) for user in users]
    
    def update_user(self, user_id: str, user_data: UserUpdate) -> UserResponse:
        """Actualizo usuario"""
        self.get_user(user_id)  # Verifico que existe
        
        update_expression = "SET updated_at = :updated_at"
        expression_values = {":updated_at": get_current_timestamp()}
        
        if user_data.phone is not None:
            if not validate_phone_number(user_data.phone):
                raise ValueError("Número telefónico inválido")
            update_expression += ", phone = :phone"
            expression_values[":phone"] = format_phone_number(user_data.phone)
        
        if user_data.notification_preference is not None:
            update_expression += ", notification_preference = :notification_preference"
            expression_values[":notification_preference"] = user_data.notification_preference.value
        
        db_service.update_item(
            self.table_name,
            {"user_id": user_id},
            update_expression,
            expression_values
        )
        
        return self.get_user(user_id)
    
    def validate_balance(self, user_id: str, amount: float, fund_name: str) -> None:
        """Valido que el usuario tenga saldo suficiente"""
        user = self.get_user(user_id)
        if user.balance < amount:
            raise InsufficientBalanceException(fund_name)

# Instancia global del servicio
user_service = UserService()