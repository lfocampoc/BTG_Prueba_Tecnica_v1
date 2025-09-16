"""
Handler para AWS Lambda con FastAPI
BTG Pactual - Funds API
"""

import json
import logging
from mangum import Mangum
from src.api.main import app

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Handler para Lambda usando Mangum
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    Handler principal para AWS Lambda
    """
    try:
        logger.info(f"Evento recibido: {json.dumps(event)}")
        response = handler(event, context)
        logger.info(f"Respuesta generada: {json.dumps(response)}")
        return response
    except Exception as e:
        logger.error(f"Error en Lambda: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error interno del servidor"})
        }
