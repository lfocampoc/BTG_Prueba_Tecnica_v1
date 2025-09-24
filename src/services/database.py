import boto3
from boto3.dynamodb.conditions import Key
from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal
from src.config import settings
from src.utils import get_current_timestamp

class DynamoDBService:
    def __init__(self):
        # En Lambda, usar el rol IAM asignado automáticamente
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.aws_region)
        self.tables = {
            'users': self.dynamodb.Table(settings.dynamodb_table_users),
            'funds': self.dynamodb.Table(settings.dynamodb_table_funds),
            'subscriptions': self.dynamodb.Table(settings.dynamodb_table_subscriptions),
            'transactions': self.dynamodb.Table(settings.dynamodb_table_transactions),
            'notifications': self.dynamodb.Table(settings.dynamodb_table_notifications)
        }
    
    def _convert_floats_to_decimal(self, obj):
        """Convierto floats a Decimal para compatibilidad con DynamoDB"""
        if isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, dict):
            return {key: self._convert_floats_to_decimal(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_floats_to_decimal(item) for item in obj]
        else:
            return obj
    
    def create_item(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """Creo un nuevo elemento en la tabla"""
        table = self.tables[table_name]
        # Solo agrego created_at si no existe (para no sobrescribir el del servicio)
        if 'created_at' not in item:
            item['created_at'] = get_current_timestamp()
        # Convierto floats a Decimal antes de guardar
        converted_item = self._convert_floats_to_decimal(item)
        table.put_item(Item=converted_item)
        return item
    
    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Obtengo un elemento por su clave"""
        table = self.tables[table_name]
        response = table.get_item(Key=key)
        return response.get('Item')
    
    def update_item(self, table_name: str, key: Dict[str, Any], 
                   update_expression: str, expression_values: Dict[str, Any],
                   expression_attribute_names: Dict[str, str] = None) -> Dict[str, Any]:
        """Actualizo un elemento"""
        table = self.tables[table_name]
        # Solo agrego updated_at si no está en la expresión (para no sobrescribir el del servicio)
        if ':updated_at' not in expression_values:
            expression_values[':updated_at'] = get_current_timestamp()
            update_expression += ", updated_at = :updated_at"
        
        # Convierto floats a Decimal en los valores de expresión
        converted_values = self._convert_floats_to_decimal(expression_values)
        
        update_kwargs = {
            'Key': key,
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': converted_values,
            'ReturnValues': "UPDATED_NEW"
        }
        
        if expression_attribute_names:
            update_kwargs['ExpressionAttributeNames'] = expression_attribute_names
        
        response = table.update_item(**update_kwargs)
        return response
    
    def query_items(self, table_name: str, key_condition_expression: str, 
                   expression_values: Dict[str, Any], index_name: str = None) -> List[Dict[str, Any]]:
        """Consulto elementos con condición de clave"""
        table = self.tables[table_name]
        # Convierto floats a Decimal en los valores de expresión
        converted_values = self._convert_floats_to_decimal(expression_values)
        
        query_kwargs = {
            'KeyConditionExpression': key_condition_expression,
            'ExpressionAttributeValues': converted_values
        }
        
        # Si se especifica un índice, lo uso
        if index_name:
            query_kwargs['IndexName'] = index_name
            
        response = table.query(**query_kwargs)
        return response.get('Items', [])
    
    def scan_items(self, table_name: str, filter_expression: str = None, 
                  expression_values: Dict[str, Any] = None, 
                  expression_attribute_names: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """Escaneo todos los elementos de una tabla"""
        table = self.tables[table_name]
        scan_kwargs = {}
        if filter_expression and expression_values:
            scan_kwargs['FilterExpression'] = filter_expression
            # Convierto floats a Decimal en los valores de expresión
            scan_kwargs['ExpressionAttributeValues'] = self._convert_floats_to_decimal(expression_values)
        
        if expression_attribute_names:
            scan_kwargs['ExpressionAttributeNames'] = expression_attribute_names
        
        response = table.scan(**scan_kwargs)
        return response.get('Items', [])

# Instancia global del servicio
db_service = DynamoDBService()