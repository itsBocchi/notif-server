# Sistema de Alertas de Emergencia - Arquitectura de Microservicios

## 🏗️ Arquitectura del Sistema

El sistema ha sido refactorizado de un monolito a una **arquitectura de microservicios** especializada, dividida en 4 servicios independientes:

```
┌─────────────────────────────────────────────────────────┐
│                    API GATEWAY                          │
│              (Load Balancer + Routing)                 │
└─────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
┌───────────────────▼─┐ ┌─────▼─────┐ ┌─▼─────────────────────┐
│ Alert Management   │ │   Auth    │ │ Geospatial          │
│ Service (Core)     │ │ Service   │ │ Service             │
│                    │ │           │ │                     │
│ • CRUD Alertas     │ │ • API Keys│ │ • Coordenadas       │
│ • Clasificación    │ │ • Permisos│ │ • Radios            │
│ • Orquestación     │ │ • Validar │ │ • Evacuación        │
└────────────────────┘ └───────────┘ └─────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Notification      │
                    │ Delivery Service  │
                    │                   │
                    │ • FCM             │
                    │ • WebSocket       │
                    │ • Webhooks        │
                    └───────────────────┘
```

## 🔧 Microservicios

### 1. Alert Management Service (Core) - `/api/`
**Responsabilidad**: Gestión central de alertas y orquestación
- CRUD completo de alertas de emergencia
- Clasificación por tipo de catástrofe
- Coordinación entre microservicios
- Almacenamiento en SQLite local y Firebase Firestore

### 2. Authentication Service - `/auth/`
**Responsabilidad**: Autenticación y autorización
- Gestión de API keys UUID
- Validación de permisos (usuario/admin)
- Creación y revocación de credenciales
- Trazabilidad de operaciones

### 3. Geospatial Service - `/geo/`
**Responsabilidad**: Procesamiento geoespacial
- Validación de coordenadas geográficas
- Cálculo de radios de evacuación
- Determinación de puntos de evacuación
- Algoritmos especializados por tipo de emergencia

### 4. Notification Service - `/notifications/`
**Responsabilidad**: Entrega multi-canal de notificaciones
- Firebase Cloud Messaging (FCM)
- WebSocket para tiempo real
- Webhooks para sistemas externos
- Broadcast coordinado multi-canal

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Django 4.2+
- Firebase Admin SDK
- Archivo `serviceAccountKey.json`

### Configuración Rápida

```bash
# 1. Clonar y configurar entorno
git clone <tu-repositorio>
cd notif-server
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Configurar Firebase
# Colocar serviceAccountKey.json en la raíz del proyecto

# 3. Configurar microservicios (automático)
python setup_microservices.py

# 4. Ejecutar servidor
python manage.py runserver
```

### Configuración Manual

```bash
# Crear migraciones para cada servicio
python manage.py makemigrations auth_service
python manage.py makemigrations server
python manage.py migrate

# Crear API key de administrador
python create_admin_api_key.py "ONEMI Admin"

# Ejecutar pruebas
python run_tests.py
```

## 📡 Endpoints por Microservicio

### Alert Management Service (`/api/`)
```
POST   /api/send-notification/     # Enviar alerta
GET    /api/alerts/                # Listar alertas
GET    /api/alerts/{id}/           # Obtener alerta
PUT    /api/alerts/{id}/update/    # Actualizar alerta (admin)
DELETE /api/alerts/{id}/delete/    # Eliminar alerta (admin)
```

### Authentication Service (`/auth/`)
```
POST /auth/validate/               # Validar API key
GET  /auth/api-keys/               # Listar API keys (admin)
POST /auth/api-keys/create/        # Crear API key (admin)
PUT  /auth/api-keys/{id}/revoke/   # Revocar API key (admin)
```

### Geospatial Service (`/geo/`)
```
POST /geo/validate-coordinates/        # Validar coordenadas
POST /geo/calculate-evacuation-zone/   # Calcular zona completa
POST /geo/calculate-evacuation-radius/ # Calcular radio
POST /geo/find-evacuation-points/      # Encontrar puntos
```

### Notification Service (`/notifications/`)
```
POST /notifications/send/         # Enviar por canal específico
POST /notifications/broadcast/    # Broadcast multi-canal
POST /notifications/firebase/     # Solo Firebase FCM
POST /notifications/websocket/    # Solo WebSocket
```

## 🔐 Sistema de Permisos

### Usuario Normal
- ✅ Enviar alertas
- ✅ Consultar alertas
- ✅ Usar servicios geoespaciales
- ✅ Enviar notificaciones

### Administrador
- ✅ Todas las operaciones de usuario normal
- ✅ Actualizar/eliminar alertas
- ✅ Gestionar API keys
- ✅ Validar credenciales de otros usuarios

## 🧪 Testing

### Ejecutar Todas las Pruebas
```bash
python run_tests.py
```

### Pruebas por Microservicio
```bash
python manage.py test auth_service
python manage.py test api
python manage.py test server
```

### Pruebas de Integración
```bash
# Probar flujo completo de alerta
python test_fire_alert.py <api-key> "Test Fire" "Test Description" -33.037542 -71.485482 true

# Probar servicios geoespaciales
curl -X POST http://localhost:8000/geo/validate-coordinates/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{"latitude": -33.037542, "longitude": -71.485482}'
```

## 📊 Beneficios de la Arquitectura

### Escalabilidad
- Cada servicio puede escalar independientemente según demanda
- Auth Service: Por número de usuarios
- Geospatial Service: Por complejidad de cálculos
- Notification Service: Por volumen de mensajes

### Mantenibilidad
- Cambios aislados por dominio de responsabilidad
- Equipos especializados por servicio
- Ciclos de release independientes

### Reutilización
- Auth Service: Reutilizable en otros sistemas gubernamentales
- Geospatial Service: Aplicable a múltiples dominios (tráfico, urbanismo)
- Notification Service: Configurable para diferentes tipos de comunicación

### Tolerancia a Fallos
- Fallo en notificaciones no afecta creación de alertas
- Fallo en geolocalización no impide alertas básicas
- Degradación gradual del servicio

## 🔄 Migración desde Monolito

El sistema mantiene **compatibilidad hacia atrás** con la API original:
- `/api/send-notification/` sigue funcionando igual
- Internamente orquesta los microservicios
- Respuestas incluyen información adicional de cada servicio

## 📈 Monitoreo y Observabilidad

### Logs por Servicio
```bash
# Ver logs específicos por servicio
python manage.py shell
>>> import logging
>>> logger = logging.getLogger('auth_service')
>>> logger.info("Testing auth service logging")
```

### Health Checks
Cada servicio expone endpoints de salud para monitoreo:
- Validación de conectividad a Firebase
- Estado de base de datos
- Métricas de rendimiento

## 🚀 Próximos Pasos

### Deployment en Producción
- Containerización con Docker
- Orquestación con Kubernetes
- Load balancing por servicio
- Monitoreo con Prometheus/Grafana

### Funcionalidades Futuras
- Circuit breakers entre servicios
- Rate limiting por servicio
- Caché distribuido (Redis)
- Event sourcing para trazabilidad completa

---

Para más detalles, consulta la [documentación completa de la API](API_EXAMPLES.md).