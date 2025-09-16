#!/usr/bin/env python3
"""
Script para crear el administrador inicial del sistema
Solo se ejecuta una vez al configurar el sistema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.user_service import user_service
from src.models.user import UserCreate, UserRole, NotificationPreference

def create_admin():
    """Creo el administrador inicial del sistema"""
    admin_email = "admin@gtc.com"
    admin_password = "123456"
    
    try:
        # Verifico si ya existe un admin
        existing_admin = user_service.get_user_by_email(admin_email)
        if existing_admin:
            print(f"✅ El administrador {admin_email} ya existe")
            return existing_admin
        
        # Creo el admin
        admin_data = UserCreate(
            email=admin_email,
            phone="+573001234567",
            password=admin_password,
            notification_preference=NotificationPreference.EMAIL
        )
        
        admin = user_service.create_user(admin_data, role=UserRole.ADMIN)
        print(f"✅ Administrador creado exitosamente:")
        print(f"   Email: {admin.email}")
        print(f"   User ID: {admin.user_id}")
        print(f"   Role: {admin.role}")
        print(f"   Balance: ${admin.balance:,.2f} COP")
        print(f"   ⚠️  Cambiar contraseña en producción!")
        
        return admin
        
    except Exception as e:
        print(f"❌ Error creando administrador: {e}")
        return None

if __name__ == "__main__":
    print("🔧 Inicializando administrador del sistema...")
    create_admin()
