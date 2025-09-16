# Scripts SQL - BTG Database

Este directorio contiene los scripts SQL para la **Parte 2** de la prueba técnica BTG Pactual.

## 📁 Archivos Incluidos

- `01_crear_database.sql` - Script de creación de base de datos y tablas
- `02_data_database.sql` - Datos de prueba para testing
- `03_query_tablas.sql` - Consulta SQL compleja requerida
- `README.md` - Este archivo de documentación

## 🚀 Instalación y Ejecución

### Prerrequisitos
- PostgreSQL 12+ instalado
- Usuario con permisos de administrador
- Acceso a línea de comandos

### Pasos de Instalación

#### Opción A: Usando pgAdmin (Recomendado)

1. **Ejecutar script completo:**
   - Abrir pgAdmin
   - Conectarse a PostgreSQL (base de datos `postgres`)
   - Ejecutar `01_crear_database.sql` (crea BD y tablas automáticamente)
   - Conectarse a la base de datos `btg` creada
   - Ejecutar `02_data_database.sql` (insertar datos)
   - Ejecutar `03_query_tablas.sql` (consulta compleja)

#### Opción B: Usando psql (Línea de comandos)

1. **Crear la base de datos:**
```bash
psql -U postgres -f 01_crear_database.sql
```

2. **Insertar datos de prueba:**
```bash
psql -U postgres -d btg -f 02_data_database.sql
```

3. **Ejecutar consulta compleja:**
```bash
psql -U postgres -d btg -f 03_query_tablas.sql
```

### Ejecución Manual

```bash
# Conectar a PostgreSQL
psql -U postgres

# Ejecutar scripts paso a paso
\i 01_crear_database.sql
\i 02_data_database.sql
\i 03_query_tablas.sql
```

## 📊 Estructura de la Base de Datos

### Tablas Principales
- **`cliente`** - Información de clientes
- **`producto`** - Catálogo de productos
- **`sucursal`** - Sucursales de BTG

### Tablas de Relación
- **`inscripcion`** - Cliente ↔ Producto (suscripciones)
- **`disponibilidad`** - Sucursal ↔ Producto (disponibilidad)
- **`visitan`** - Cliente ↔ Sucursal (visitas)

## 🔍 Consulta Principal

**Objetivo:** Obtener los nombres de los clientes que tienen inscrito algún producto disponible **SOLO** en las sucursales que visitan.

**Lógica:**
1. Cliente debe tener inscripciones activas
2. Cliente debe haber visitado sucursales
3. Producto inscrito debe estar disponible en sucursales visitadas
4. Producto NO debe estar disponible en sucursales NO visitadas

## 📈 Datos de Prueba

- **10 clientes** en diferentes ciudades
- **10 productos** de diferentes tipos (FIC, FPV)
- **10 sucursales** en 5 ciudades
- **20 inscripciones** activas
- **40 registros de disponibilidad**
- **20 visitas** de clientes a sucursales

## ✅ Verificación

Los scripts incluyen consultas de verificación para:
- Conteo de registros por tabla
- Análisis de relaciones
- Ejemplos de datos específicos
- Validación de la consulta principal

## 🎯 Resultado Esperado

La consulta debe retornar clientes que cumplan la condición específica de tener productos disponibles únicamente en las sucursales que han visitado.
