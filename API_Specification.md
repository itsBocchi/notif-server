# Especificación Completa de API - Sistema de Alertas de Emergencia

## 1. POST /api/send-notification/

### Headers
```
Content-Type: application/json
X-API-Key: <uuid>
```

### Request Body
```json
{
  "title": "string (max 255 chars, required)",
  "body": "string (required)",
  "type": "incendio|earthquake|general (required)",
  "latitude": "float (optional)",
  "longitude": "float (optional)",
  "magnitude": "float (required for earthquake)",
  "active": "boolean (default: true)"
}
```

### Responses

**201 Created**
```json
{
  "id": 123,
  "message": "Alert created and sent successfully",
  "firebase_id": "abc123def456",
  "fcm_sent": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**400 Bad Request**
```json
{
  "error": "Validation failed",
  "details": {
    "title": ["This field is required"],
    "magnitude": ["Required for earthquake type"]
  }
}
```

**401 Unauthorized**
```json
{
  "error": "Invalid API key",
  "message": "Authentication required"
}
```

---

## 2. GET /api/alerts/

### Headers
```
X-API-Key: <uuid>
```

### Query Parameters
- `active`: boolean (optional)
- `type`: string (optional)
- `limit`: int (default: 20, max: 100)
- `offset`: int (default: 0)

### Responses

**200 OK**
```json
{
  "count": 25,
  "next": "/api/alerts/?offset=20&limit=20",
  "previous": null,
  "results": [
    {
      "id": 123,
      "title": "Incendio en Valparaíso",
      "body": "Incendio detectado en sector norte",
      "type": "incendio",
      "latitude": -33.037542,
      "longitude": -71.485482,
      "magnitude": null,
      "active": true,
      "source": "Bomberos de Valparaíso",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**401 Unauthorized**
```json
{
  "error": "Invalid API key",
  "message": "Authentication required"
}
```

---

## 3. GET /api/alerts/{id}/

### Headers
```
X-API-Key: <uuid>
```

### Responses

**200 OK**
```json
{
  "id": 123,
  "title": "Incendio en Valparaíso",
  "body": "Incendio detectado en sector norte de la ciudad",
  "type": "incendio",
  "latitude": -33.037542,
  "longitude": -71.485482,
  "magnitude": null,
  "active": true,
  "source": "Bomberos de Valparaíso",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**404 Not Found**
```json
{
  "error": "Alert not found",
  "message": "Alert with id 123 does not exist"
}
```

---

## 4. PUT /api/alerts/{id}/update/

### Headers
```
Content-Type: application/json
X-API-Key: <uuid> (Admin required)
```

### Request Body
```json
{
  "title": "string (optional)",
  "body": "string (optional)",
  "active": "boolean (optional)",
  "latitude": "float (optional)",
  "longitude": "float (optional)"
}
```

### Responses

**200 OK**
```json
{
  "id": 123,
  "message": "Alert updated successfully",
  "updated_fields": ["title", "active"],
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**403 Forbidden**
```json
{
  "error": "Insufficient permissions",
  "message": "Admin access required"
}
```

---

## 5. DELETE /api/alerts/{id}/delete/

### Headers
```
X-API-Key: <uuid> (Admin required)
```

### Responses

**204 No Content**
```
(Empty response body)
```

**403 Forbidden**
```json
{
  "error": "Insufficient permissions",
  "message": "Admin access required"
}
```

**404 Not Found**
```json
{
  "error": "Alert not found",
  "message": "Alert with id 123 does not exist"
}
```

---

## 6. POST /auth/validate/

### Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "api_key": "uuid-string"
}
```

### Responses

**200 OK**
```json
{
  "valid": true,
  "permissions": "user",
  "entity": "Bomberos de Valparaíso",
  "is_admin": false,
  "expires_at": null
}
```

**200 OK (Invalid Key)**
```json
{
  "valid": false,
  "message": "API key not found or inactive"
}
```

---

## 7. GET /api/api-keys/

### Headers
```
X-API-Key: <uuid> (Admin required)
```

### Responses

**200 OK**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "key": "550e8400-e29b-41d4-a716-446655440000",
      "name": "bomberos_vina_01",
      "entidad": "Bomberos de Viña del Mar",
      "is_active": true,
      "is_admin": false,
      "created_at": "2024-01-10T09:00:00Z"
    }
  ]
}
```

---

## 8. POST /api/api-keys/create/

### Headers
```
Content-Type: application/json
X-API-Key: <uuid> (Admin required)
```

### Request Body
```json
{
  "name": "string (required)",
  "entidad": "string (required)",
  "description": "string (optional)",
  "is_admin": "boolean (default: false)"
}
```

### Responses

**201 Created**
```json
{
  "id": 6,
  "key": "550e8400-e29b-41d4-a716-446655440001",
  "name": "senapred_regional",
  "entidad": "SENAPRED Región de Valparaíso",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-15T12:00:00Z"
}
```

---

## 9. PUT /api/api-keys/{id}/revoke/

### Headers
```
X-API-Key: <uuid> (Admin required)
```

### Responses

**200 OK**
```json
{
  "id": 6,
  "message": "API key revoked successfully",
  "is_active": false,
  "revoked_at": "2024-01-15T12:30:00Z"
}
```

---

## 10. POST /geo/validate-coordinates/

### Headers
```
Content-Type: application/json
X-API-Key: <uuid>
```

### Request Body
```json
{
  "latitude": -33.037542,
  "longitude": -71.485482
}
```

### Responses

**200 OK**
```json
{
  "valid": true,
  "latitude": -33.037542,
  "longitude": -71.485482,
  "region": "Valparaíso",
  "country": "Chile"
}
```

**400 Bad Request**
```json
{
  "valid": false,
  "error": "Invalid coordinates",
  "message": "Latitude must be between -90 and 90"
}
```

---

## 11. POST /geo/calculate-evacuation-zone/

### Headers
```
Content-Type: application/json
X-API-Key: <uuid>
```

### Request Body
```json
{
  "latitude": -33.037542,
  "longitude": -71.485482,
  "type": "incendio|earthquake"
}
```

### Responses

**200 OK**
```json
{
  "center": {
    "latitude": -33.037542,
    "longitude": -71.485482
  },
  "radius_meters": 500,
  "evacuation_points": [
    {
      "latitude": -33.038000,
      "longitude": -71.486000,
      "name": "Plaza Principal"
    }
  ],
  "zone_polygon": [
    [-33.037000, -71.485000],
    [-33.038000, -71.485000],
    [-33.038000, -71.486000],
    [-33.037000, -71.486000]
  ]
}
```

---

## 12. POST /geo/calculate-evacuation-radius/

### Headers
```
Content-Type: application/json
X-API-Key: <uuid>
```

### Request Body
```json
{
  "type": "incendio|earthquake"
}
```

### Responses

**200 OK**
```json
{
  "type": "incendio",
  "radius_meters": 1,
  "description": "Radio de evacuación para incendios"
}
```

---

## 13. POST /geo/find-evacuation-points/

### Headers
```
Content-Type: application/json
X-API-Key: <uuid>
```

### Request Body
```json
{
  "latitude": -33.037542,
  "longitude": -71.485482,
  "radius_km": 2
}
```

### Responses

**200 OK**
```json
{
  "evacuation_points": [
    {
      "latitude": -33.038000,
      "longitude": -71.486000,
      "name": "Plaza Principal",
      "distance_meters": 150,
      "capacity": 500
    },
    {
      "latitude": -33.039000,
      "longitude": -71.487000,
      "name": "Estadio Municipal",
      "distance_meters": 300,
      "capacity": 2000
    }
  ],
  "total_points": 2
}
```

## Códigos de Estado HTTP Comunes

| Código | Descripción | Cuándo se usa |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Eliminación exitosa |
| 400 | Bad Request | Datos de entrada inválidos |
| 401 | Unauthorized | API Key faltante o inválida |
| 403 | Forbidden | Permisos insuficientes |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error interno del servidor |

## Headers Comunes

### Requeridos para autenticación
```
X-API-Key: <uuid>
```

### Para requests con body
```
Content-Type: application/json
```

### Respuestas del servidor
```
Content-Type: application/json
X-RateLimit-Remaining: 100
X-Response-Time: 0.234ms
```