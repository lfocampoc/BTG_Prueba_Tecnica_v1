import uuid
from datetime import datetime
from typing import Dict, Any
import json

def generate_id(prefix: str = "") -> str:
    """Genero un ID único con prefijo opcional"""
    unique_id = str(uuid.uuid4())
    return f"{prefix}_{unique_id}" if prefix else unique_id

def get_current_timestamp() -> str:
    """Obtengo el timestamp actual en formato ISO"""
    return datetime.utcnow().isoformat()

def format_currency(amount: float) -> str:
    """Formateo el monto como moneda colombiana"""
    return f"COP ${amount:,.2f}"

def validate_phone_number(phone: str) -> bool:
    """Valido el formato de número telefónico colombiano"""
    # Limpio espacios y caracteres especiales
    clean_phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Verifico que empiece con +57 o 57
    if clean_phone.startswith("+57"):
        clean_phone = clean_phone[3:]
    elif clean_phone.startswith("57"):
        clean_phone = clean_phone[2:]
    
    # Verifico que tenga 10 dígitos
    return clean_phone.isdigit() and len(clean_phone) == 10

def format_phone_number(phone: str) -> str:
    """Formateo el número telefónico a formato estándar"""
    clean_phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    if clean_phone.startswith("+57"):
        return clean_phone
    elif clean_phone.startswith("57"):
        return f"+{clean_phone}"
    else:
        return f"+57{clean_phone}"

def create_error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
    """Crear respuesta de error estandarizada"""
    return {
        "error": True,
        "message": message,
        "status_code": status_code,
        "timestamp": get_current_timestamp()
    }

def create_success_response(data: Any, message: str = "Operación exitosa") -> Dict[str, Any]:
    """Crear respuesta de éxito estandarizada"""
    return {
        "error": False,
        "message": message,
        "data": data,
        "timestamp": get_current_timestamp()
    }