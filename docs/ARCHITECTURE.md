# Arquitectura del Sistema de Alertas de Emergencia

## Componentes del Sistema

### 1. API Gateway (`api/views.py`)
- **Responsabilidad**: Punto de entrada único para todas las peticiones
- **Funciones**:
  - Validación de headers HTTP
  - Enrutamiento de peticiones
  - Manejo de errores HTTP
- **Endpoint principal**: `POST /api/send-notification/`

### 2. Sistema de Autenticación (`server/models.py - ApiKey`)
- **Responsabilidad**: Gestión de credenciales y autorización
- **Funciones**:
  - Generación de API keys UUID
  - Validación de tokens de acceso
  - Gestión de permisos por organismo
- **Modelo**: `ApiKey` con campos key, name, description, is_active

### 3. Procesador de Alertas (`api/views.py - send_notification`)
- **Responsabilidad**: Validación y estructuración de datos de emergencia
- **Funciones**:
  - Validación de campos obligatorios
  - Clasificación por tipo de emergencia
  - Preparación de datos para almacenamiento
- **Tipos soportados**: `incendio`, `earthquake`, `general`

### 4. Gestor Geoespacial (`firebase_utils.py`)
- **Responsabilidad**: Procesamiento de datos geográficos
- **Funciones**:
  - Validación de coordenadas
  - Cálculo de radios de evacuación
  - Determinación de puntos de evacuación
- **Parámetros por defecto**:
  - Incendios: 1 metro de radio
  - Terremotos: 500 metros de radio

### 5. Almacén de Datos (`firebase_utils.py + server/models.py`)
- **Responsabilidad**: Persistencia dual (local + nube)
- **Componentes**:
  - **Local**: SQLite con modelo `Notification`
  - **Nube**: Firebase Firestore colección `alertas`
- **Estructura Firestore**:
  ```json
  {
    "activo": boolean,
    "puntos_evacuacion": [{"latitude": float, "longitude": float}],
    "radios_evacuacion": [number],
    "time": timestamp,
    "title": string,
    "body": string,
    "type": string,
    "magnitude": float (solo terremotos)
  }
  ```

## Flujo de Datos

1. **Recepción**: API Gateway recibe petición HTTP POST
2. **Autenticación**: Sistema valida API key en header X-API-Key
3. **Procesamiento**: Procesador de Alertas valida y estructura datos
4. **Geolocalización**: Gestor Geoespacial procesa coordenadas
5. **Persistencia**: Almacén de Datos guarda en SQLite y Firestore
6. **Notificación**: Sistema envía a Firebase Cloud Messaging
7. **WebSocket**: Notificación en tiempo real a clientes conectados

## Seguridad

- **Autenticación**: API keys UUID únicos por organismo
- **Autorización**: Validación de claves activas en cada petición
- **Trazabilidad**: Registro de fuente en cada alerta
- **Validación**: Campos obligatorios y tipos de datos

## Escalabilidad

- **Base de datos**: Firebase Firestore con escalado automático
- **API**: Django con capacidad de múltiples workers
- **Almacenamiento**: Dual (local para auditoría, nube para disponibilidad)
- **Comunicación**: WebSockets para notificaciones en tiempo real