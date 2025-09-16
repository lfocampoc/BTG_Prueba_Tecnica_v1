from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración de AWS
    aws_region: str = "us-east-2"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    
    # Configuración de JWT
    secret_key: str = "btg-funds-secret-key-2025"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuración de la aplicación
    app_name: str = "BTG Pactual Funds API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Reglas de negocio
    initial_balance: float = 500000.0  # COP $500.000
    
    # Tablas de DynamoDB
    dynamodb_table_users: str = "gtc-users"
    dynamodb_table_funds: str = "gtc-funds"
    dynamodb_table_subscriptions: str = "gtc-subscriptions"
    dynamodb_table_transactions: str = "gtc-transactions"
    dynamodb_table_notifications: str = "gtc-notifications"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignoro variables extra

settings = Settings()