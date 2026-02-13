# Sistema de Alertas de Emergencia - Arquitectura de Microservicios

Este documento proporciona la documentación completa del sistema basado en microservicios para gestión de alertas de emergencia.

## Arquitectura del Sistema

El sistema está dividido en 4 microservicios especializados:

- **Alert Management Service** (Core): Gestión CRUD de alertas
- **Authentication Service**: Autenticación y autorización
- **Geospatial Service**: Procesamiento de datos geoespaciales
- **Notification Service**: Entrega de notificaciones multi-canal

## Requisitos

- Una API key válida (obtenida del Authentication Service)
- El servidor de notificaciones debe estar en ejecución
- Para operaciones administrativas: API key con permisos de admin

## Ejemplos

### 1. Alerta de Incendio

#### Usando curl

```bash
curl -X POST http://localhost:8000/api/send-notification/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "title": "USM Sede Viña del Mar",
    "body": "Incendio detectado en el campus",
    "topic": "incendio",
    "type": "incendio",
    "latitude": -33.037542,
    "longitude": -71.485482,
    "active": true
  }'
```

#### Usando PowerShell

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "tu-api-key"
}

$body = @{
    title = "USM Sede Viña del Mar"
    body = "Incendio detectado en el campus"
    topic = "incendio"
    type = "incendio"
    latitude = -33.037542
    longitude = -71.485482
    active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/send-notification/" -Method Post -Headers $headers -Body $body
```

#### Usando Python

```python
import requests
import json

api_key = "tu-api-key"
url = "http://localhost:8000/api/send-notification/"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key
}

data = {
    "title": "USM Sede Viña del Mar",
    "body": "Incendio detectado en el campus",
    "topic": "incendio",
    "type": "incendio",
    "latitude": -33.037542,
    "longitude": -71.485482,
    "active": True
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
```

### 2. Alerta de Terremoto

#### Usando curl

```bash
curl -X POST http://localhost:8000/api/send-notification/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "title": "Quilpué, Chile",
    "body": "Terremoto de magnitud 7.5",
    "topic": "earthquake",
    "type": "earthquake",
    "magnitude": 7.5,
    "latitude": -33.050708,
    "longitude": -71.435072,
    "active": false
  }'
```

#### Usando PowerShell

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "tu-api-key"
}

$body = @{
    title = "Quilpué, Chile"
    body = "Terremoto de magnitud 7.5"
    topic = "earthquake"
    type = "earthquake"
    magnitude = 7.5
    latitude = -33.050708
    longitude = -71.435072
    active = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/send-notification/" -Method Post -Headers $headers -Body $body
```

#### Usando Python

```python
import requests
import json

api_key = "tu-api-key"
url = "http://localhost:8000/api/send-notification/"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key
}

data = {
    "title": "Quilpué, Chile",
    "body": "Terremoto de magnitud 7.5",
    "topic": "earthquake",
    "type": "earthquake",
    "magnitude": 7.5,
    "latitude": -33.050708,
    "longitude": -71.435072,
    "active": False
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
```

## Scripts de Prueba Incluidos

El sistema incluye scripts para probar fácilmente el envío de alertas:

### Para alertas de incendio:

```bash
python test_fire_alert.py <api_key> "USM Sede Viña del Mar" "Incendio detectado" -33.037542 -71.485482 true
```

### Para alertas de terremoto:

```bash
python test_earthquake_alert.py <api_key> "Quilpué, Chile" "Terremoto de magnitud 7.5" 7.5 -33.050708 -71.435072 false
```

## Nuevos Endpoints de la API

### Gestión de Alertas

#### Listar Alertas
```bash
curl -X GET http://localhost:8000/api/alerts/ \
  -H "X-API-Key: tu-api-key"
```

#### Obtener Alerta Específica
```bash
curl -X GET http://localhost:8000/api/alerts/1/ \
  -H "X-API-Key: tu-api-key"
```

#### Actualizar Alerta (requiere admin)
```bash
curl -X PUT http://localhost:8000/api/alerts/1/update/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-admin-api-key" \
  -d '{
    "title": "Título Actualizado",
    "body": "Descripción actualizada",
    "topic": "updated"
  }'
```

#### Eliminar Alerta (requiere admin)
```bash
curl -X DELETE http://localhost:8000/api/alerts/1/delete/ \
  -H "X-API-Key: tu-admin-api-key"
```

## Microservicios Disponibles

### 1. Authentication Service (`/auth/`)

#### Validar API Key
```bash
curl -X POST http://localhost:8000/auth/validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "tu-api-key",
    "require_admin": false
  }'
```

#### Listar API Keys (Admin)
```bash
curl -X GET http://localhost:8000/auth/api-keys/ \
  -H "X-API-Key: tu-admin-api-key"
```

#### Crear Nueva API Key (Admin)
```bash
curl -X POST http://localhost:8000/auth/api-keys/create/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-admin-api-key" \
  -d '{
    "name": "Nueva Organización",
    "description": "Descripción de la nueva API key",
    "is_admin": false
  }'
```

#### Revocar API Key (Admin)
```bash
curl -X PUT http://localhost:8000/auth/api-keys/1/revoke/ \
  -H "X-API-Key: tu-admin-api-key"
```

### 2. Geospatial Service (`/geo/`)

#### Validar Coordenadas
```bash
curl -X POST http://localhost:8000/geo/validate-coordinates/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "latitude": -33.037542,
    "longitude": -71.485482
  }'
```

#### Calcular Zona de Evacuación
```bash
curl -X POST http://localhost:8000/geo/calculate-evacuation-zone/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "latitude": -33.037542,
    "longitude": -71.485482,
    "emergency_type": "incendio",
    "magnitude": 7.5
  }'
```

#### Calcular Radio de Evacuación
```bash
curl -X POST http://localhost:8000/geo/calculate-evacuation-radius/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "emergency_type": "earthquake",
    "magnitude": 7.5
  }'
```

#### Encontrar Puntos de Evacuación
```bash
curl -X POST http://localhost:8000/geo/find-evacuation-points/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "latitude": -33.037542,
    "longitude": -71.485482,
    "emergency_type": "incendio",
    "radius": 500
  }'
```

### 3. Notification Service (`/notifications/`)

#### Enviar Notificación por Canal Específico
```bash
curl -X POST http://localhost:8000/notifications/send/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "title": "Alerta de Emergencia",
    "body": "Descripción de la alerta",
    "channel": "firebase",
    "topic": "emergencias",
    "data": {
      "type": "incendio",
      "priority": "high"
    }
  }'
```

#### Broadcast Multi-Canal
```bash
curl -X POST http://localhost:8000/notifications/broadcast/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "title": "Alerta Crítica",
    "body": "Evacuación inmediata requerida",
    "channels": {
      "firebase": {
        "enabled": true,
        "topic": "critical_alerts",
        "data": {"priority": "critical"}
      },
      "websocket": {
        "enabled": true,
        "group": "emergency_notifications",
        "data": {"urgent": true}
      },
      "webhooks": {
        "enabled": true,
        "urls": ["https://external-system.com/webhook"],
        "data": {"source": "emergency_system"}
      }
    }
  }'
```

#### Enviar Solo por Firebase
```bash
curl -X POST http://localhost:8000/notifications/firebase/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "title": "Notificación Firebase",
    "body": "Mensaje específico para Firebase",
    "topic": "firebase_topic",
    "data": {"custom_field": "value"}
  }'
```

#### Enviar Solo por WebSocket
```bash
curl -X POST http://localhost:8000/notifications/websocket/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "title": "Notificación WebSocket",
    "body": "Mensaje en tiempo real",
    "group": "realtime_updates",
    "data": {"timestamp": "2024-01-01T12:00:00Z"}
  }'
```

## Códigos de Respuesta

- `200 OK`: Operación exitosa
- `400 Bad Request`: Datos inválidos o faltantes
- `401 Unauthorized`: API key faltante o inválida
- `403 Forbidden`: Permisos insuficientes (requiere admin)
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Ejemplos con Python

### Listar Alertas
```python
import requests

api_key = "tu-api-key"
url = "http://localhost:8000/api/alerts/"

headers = {"X-API-Key": api_key}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    alerts = response.json()['alerts']
    print(f"Total de alertas: {len(alerts)}")
    for alert in alerts:
        print(f"- {alert['title']} ({alert['created_at']})")
else:
    print(f"Error: {response.json()}")
```

### Usar Servicios Geoespaciales
```python
import requests
import json

api_key = "tu-api-key"

# Validar coordenadas
url = "http://localhost:8000/geo/validate-coordinates/"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key
}
data = {
    "latitude": -33.037542,
    "longitude": -71.485482
}

response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    result = response.json()
    print(f"Coordenadas válidas: {result['valid']}")
    if result['valid']:
        print(f"Lat: {result['coordinates']['latitude']}")
        print(f"Lng: {result['coordinates']['longitude']}")
else:
    print(f"Error: {response.json()}")

# Calcular zona de evacuación completa
url = "http://localhost:8000/geo/calculate-evacuation-zone/"
data = {
    "latitude": -33.037542,
    "longitude": -71.485482,
    "emergency_type": "earthquake",
    "magnitude": 7.5
}

response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    result = response.json()
    print(f"Radio de evacuación: {result['evacuation_radius_meters']} metros")
    print(f"Puntos de evacuación encontrados: {len(result['evacuation_points'])}")
    for point in result['evacuation_points']:
        print(f"- {point['direction']}: ({point['latitude']}, {point['longitude']})")
else:
    print(f"Error: {response.json()}")
```

### Crear API Key (Admin)
```python
import requests
import json

admin_api_key = "tu-admin-api-key"
url = "http://localhost:8000/auth/api-keys/create/"  # Cambiado a auth service

headers = {
    "Content-Type": "application/json",
    "X-API-Key": admin_api_key
}

data = {
    "name": "Bomberos de Valparaíso",
    "description": "API key para el cuerpo de bomberos",
    "is_admin": False
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print(f"Nueva API key creada: {result['api_key']}")
    print(f"Organización: {result['name']}")
else:
    print(f"Error: {response.json()}")
```

### Enviar Notificaciones Multi-Canal
```python
import requests
import json

api_key = "tu-api-key"
url = "http://localhost:8000/notifications/broadcast/"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key
}

data = {
    "title": "Alerta de Terremoto",
    "body": "Terremoto de magnitud 7.5 detectado. Busque refugio inmediatamente.",
    "channels": {
        "firebase": {
            "enabled": True,
            "topic": "earthquake_alerts",
            "data": {
                "magnitude": "7.5",
                "priority": "critical",
                "action_required": "seek_shelter"
            }
        },
        "websocket": {
            "enabled": True,
            "group": "emergency_dashboard",
            "data": {
                "alert_type": "earthquake",
                "severity": "high",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        },
        "webhooks": {
            "enabled": True,
            "urls": [
                "https://emergency-response.gov.cl/webhook",
                "https://mobile-app-backend.com/alerts"
            ],
            "data": {
                "source": "seismic_monitoring",
                "coordinates": {
                    "lat": -33.050708,
                    "lng": -71.435072
                }
            }
        }
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print(f"Notificación enviada exitosamente")
    print(f"Canales exitosos: {result['successful_channels']}/{result['total_channels']}")
    
    # Mostrar resultados por canal
    for channel, channel_result in result['results'].items():
        status = "✓" if channel_result['success'] else "✗"
        print(f"{status} {channel.capitalize()}: {channel_result.get('message_id', 'N/A')}")
else:
    print(f"Error: {response.json()}")
```

## Configuración Inicial

### Crear API Key de Administrador
```bash
python create_admin_api_key.py "ONEMI" "API key principal para administradores"
```

### Ejecutar Pruebas
```bash
python run_tests.py
```

## Arquitectura de Microservicios

### Servicios Disponibles

| Servicio | Puerto/Ruta | Responsabilidad |
|----------|-------------|----------------|
| **Alert Management** | `/api/` | CRUD de alertas, orquestación |
| **Authentication** | `/auth/` | Gestión de API keys y permisos |
| **Geospatial** | `/geo/` | Cálculos geoespaciales y evacuación |
| **Notification** | `/notifications/` | Entrega multi-canal de notificaciones |

### Flujo de Comunicación

```
Cliente → Alert Management (Core)
   │
   ├── Authentication Service (validación)
   │
   ├── Geospatial Service (coordenadas)
   │
   └── Notification Service (entrega)
```

### Estructura de Permisos

- **Usuario Normal**: 
  - Enviar alertas (`/api/send-notification/`)
  - Consultar alertas (`/api/alerts/`)
  - Usar servicios geoespaciales (`/geo/*`)
  - Enviar notificaciones (`/notifications/*`)

- **Administrador**: Todas las operaciones anteriores más:
  - Actualizar/eliminar alertas (`/api/alerts/*/update|delete/`)
  - Gestionar API keys (`/auth/api-keys/*`)
  - Validar credenciales (`/auth/validate/`)

### Beneficios de la Arquitectura

- **Escalabilidad**: Cada servicio puede escalar independientemente
- **Mantenibilidad**: Cambios aislados por dominio de responsabilidad
- **Reutilización**: Servicios pueden ser usados por otros sistemas
- **Tolerancia a fallos**: Fallo en un servicio no compromete todo el sistema
- **Especialización**: Cada servicio optimizado para su función específica

### Configuración de Desarrollo

```bash
# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones para todos los servicios
python manage.py makemigrations auth_service
python manage.py makemigrations server
python manage.py migrate

# Crear API key de administrador
python create_admin_api_key.py "ONEMI Admin"

# Ejecutar servidor (todos los microservicios)
python manage.py runserver
```

### Testing de Microservicios

```bash
# Ejecutar todas las pruebas
python run_tests.py

# Probar servicios individuales
python manage.py test auth_service
python manage.py test geospatial_service
python manage.py test notification_service
```