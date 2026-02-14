# Endpoints del Sistema de Alertas de Emergencia

## Tabla de Endpoints

| Endpoint | Método | Permisos | Caso de Uso | Descripción |
|----------|--------|----------|-------------|-------------|
| /api/send-notification/ | POST | User | CU-01 | Envío de alertas de emergencia |
| /api/alerts/ | GET | User | CU-02 | Listado de alertas existentes |
| /api/alerts/{id}/ | GET | User | CU-02 | Consulta de alerta específica |
| /api/alerts/{id}/update/ | PUT | Admin | CU-03 | Actualización de alerta existente |
| /api/alerts/{id}/delete/ | DELETE | Admin | CU-03 | Eliminación de alerta |
| /auth/validate/ | POST | Público | CU-10 | Validar API key y verificar permisos |
| /api/api-keys/ | GET | Admin | CU-06 | Listado de API keys |
| /api/api-keys/create/ | POST | Admin | CU-06 | Creación de nueva API key |
| /api/api-keys/{id}/revoke/ | PUT | Admin | CU-06 | Revocación de API key |
| /geo/validate-coordinates/ | POST | User | CU-05 | Validar coordenadas geográficas |
| /geo/calculate-evacuation-zone/ | POST | User | CU-05 | Calcular zona completa de evacuación |
| /geo/calculate-evacuation-radius/ | POST | User | CU-05 | Calcular radio según tipo de emergencia |
| /geo/find-evacuation-points/ | POST | User | CU-05 | Encontrar puntos seguros de evacuación |

## Especificación de Endpoints Principales

### POST /api/send-notification/
**Descripción**: Crear y enviar alerta de emergencia (flujo completo)

**Request Body**:
```json
{
  "title": "string (max 255 chars)",
  "body": "string",
  "type": "incendio|earthquake|general",
  "latitude": "float (opcional)",
  "longitude": "float (opcional)",
  "magnitude": "float (solo para earthquake)",
  "active": "boolean (default: true)"
}
```

**Response (201 Created)**:
```json
{
  "id": 123,
  "message": "Alert created and sent successfully",
  "firebase_id": "abc123def456",
  "fcm_sent": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### GET /api/alerts/
**Descripción**: Listar alertas existentes con filtros opcionales

**Query Parameters**:
- `active`: boolean (filtrar por estado)
- `type`: string (filtrar por tipo)
- `limit`: int (paginación)
- `offset`: int (paginación)

**Response (200 OK)**:
```json
{
  "count": 25,
  "results": [
    {
      "id": 123,
      "title": "Incendio en Valparaíso",
      "body": "Incendio detectado en sector...",
      "type": "incendio",
      "latitude": -33.037542,
      "longitude": -71.485482,
      "active": true,
      "source": "Bomberos de Valparaíso",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### POST /auth/validate/
**Descripción**: Validar API key y obtener permisos

**Request Body**:
```json
{
  "api_key": "uuid-string"
}
```

**Response (200 OK)**:
```json
{
  "valid": true,
  "permissions": "user|admin",
  "entity": "Bomberos de Valparaíso",
  "expires_at": null
}
```

### POST /geo/validate-coordinates/
**Descripción**: Validar coordenadas geográficas

**Request Body**:
```json
{
  "latitude": -33.037542,
  "longitude": -71.485482
}
```

**Response (200 OK)**:
```json
{
  "valid": true,
  "region": "Valparaíso",
  "country": "Chile"
}
```

## Autenticación

- **Header requerido**: `X-API-Key: <uuid>`
- **Niveles de permisos**: User, Admin
- **Endpoints públicos**: Solo /auth/validate/

## Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | OK - Operación exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - API Key inválida |
| 403 | Forbidden - Permisos insuficientes |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

## Acceso Directo Firebase

| Recurso | Método | Permisos | Caso de Uso | Descripción |
|---------|--------|----------|-------------|-------------|
| Firestore /alerts | READ | Público | CU-04, CU-05 | Consulta directa desde apps móviles |

## Cambios Realizados

- **Eliminado**: `/notifications/send/` por redundancia con `/api/send-notification/`
- **Flujo simplificado**: Un endpoint crea alerta Y envía notificaciones automáticamente
- **Separación clara**: Cada endpoint tiene responsabilidad específica
- **RESTful**: Estructura consistente para recursos