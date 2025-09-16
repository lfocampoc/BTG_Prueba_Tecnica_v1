# BTG Pactual - GTC Prueba Técnica

## 📋 Descripción

API REST para gestión de fondos de inversión que permite a los clientes gestionar sus fondos sin necesidad de contactar a un asesor.

## 🎯 Funcionalidades Implementadas

### ✅ **Requisitos del PDF Cumplidos:**

1. **Suscribirse a un nuevo fondo (apertura)**
2. **Cancelar la suscripción a un fondo actual**
3. **Ver historial de transacciones (aperturas y cancelaciones)**
4. **Enviar notificación por email o SMS según preferencia del usuario**

### ✅ **Reglas de Negocio Implementadas:**

- ✅ Monto inicial del cliente: COP $500.000
- ✅ Cada transacción tiene un identificador único
- ✅ Cada fondo tiene un monto mínimo de vinculación
- ✅ Al cancelar una suscripción, el valor se retorna al cliente
- ✅ Validación de saldo suficiente con mensaje personalizado

### ✅ **Requisitos Técnicos Cumplidos:**

- ✅ **Tecnología**: Python con FastAPI
- ✅ **Base de Datos**: Modelo NoSQL (DynamoDB)
- ✅ **API REST**: Implementación completa
- ✅ **Manejo de excepciones**: Implementado
- ✅ **Código limpio**: Clean Code aplicado
- ✅ **Pruebas unitarias**: 25 tests con 74% cobertura
- ✅ **Seguridad**: JWT, encriptación SHA-256, roles
- ✅ **Despliegue**: Terraform + AWS CloudFormation
- ✅ **Documentación**: Completa incluida
- ✅ **Postman**: Colección de endpoints

## 🏗️ Arquitectura

```
Cliente → API Gateway → Lambda → DynamoDB
```

### **Componentes:**
- **API Gateway**: Punto de entrada
- **Lambda**: Lógica de negocio (FastAPI)
- **DynamoDB**: Almacenamiento NoSQL
- **IAM**: Gestión de permisos

## 🚀 Despliegue

### **Prerrequisitos:**
- AWS CLI configurado
- Terraform instalado
- Python 3.12+

### **Despliegue Rápido:**
```bash
# 1. Configurar AWS CLI
aws configure

# 2. Desplegar infraestructura
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# 3. Verificar despliegue
cd terraform
terraform output
```

## 📊 Recursos AWS

- **Lambda Function**: `btg-pactual-gtc-api-dev`
- **API Gateway**: `btg-pactual-gtc-api-dev`
- **DynamoDB Tables**: 5 tablas (users, funds, subscriptions, transactions, notifications)

## 🧪 Testing

```bash
# Ejecutar tests unitarios
python run_tests.py

# Resultado: 25 tests pasando, 74% cobertura
```

## 📝 API Endpoints

### **Autenticación:**
- `POST /api/v1/auth/register` - Registro
- `POST /api/v1/auth/login` - Login

### **Fondos:**
- `GET /api/v1/funds` - Listar fondos
- `GET /api/v1/funds/active` - Fondos activos

### **Suscripciones:**
- `POST /api/v1/subscriptions` - Suscribirse
- `GET /api/v1/subscriptions/user/{user_id}` - Ver suscripciones
- `DELETE /api/v1/subscriptions/{subscription_id}` - Cancelar

### **Transacciones:**
- `GET /api/v1/transactions/user/{user_id}` - Historial

### **Notificaciones:**
- `GET /api/v1/notifications/user/{user_id}` - Ver notificaciones

## 🔐 Seguridad

- **JWT Tokens**: Autenticación segura
- **Roles**: Client/Admin
- **Encriptación**: SHA-256
- **IAM**: Permisos específicos

## 💰 Costos

- **Free Tier**: Todos los recursos dentro del AWS Free Tier
- **Costo estimado**: $0.00/mes para uso de prueba

## 📁 Estructura del Proyecto

```
📁 GTC_Prueba_Tecnica/
├── 📁 src/                    # Código fuente
├── 📁 tests/                  # Tests unitarios
├── 📁 terraform/              # Infraestructura AWS
├── 📁 scripts/                # Scripts de despliegue
├── 📁 docs/                   # Documentación
├── 📄 lambda_handler.py       # Handler para Lambda
├── 📄 requirements.txt        # Dependencias
└── 📄 README.md              # Este archivo
```

## 🎉 Resultado Final

### **✅ Cumplimiento del PDF:**
- **100%** de funcionalidades implementadas
- **100%** de reglas de negocio cumplidas
- **100%** de requisitos técnicos satisfechos
- **Documentación completa** incluida
- **Colección Postman** para testing

### **📈 Métricas:**
- **25 tests unitarios** pasando
- **74% cobertura** de código
- **0 errores** de linting
- **Infraestructura completa** en AWS

## 📞 Información Adicional

- **Documentación técnica**: Ver `docs/README.md`
- **Arquitectura**: Ver `docs/architecture.md`
- **Colección Postman**: Ver `docs/postman_collection.json`
- **Tests**: Ejecutar `python run_tests.py`

---

**Desarrollado para BTG Pactual - Prueba Técnica GTC**
