# Patrones Arquitectónicos Implementados

## 1. API Gateway Pattern ✅

**Implementación**: Django actúa como gateway centralizando el acceso a todos los microservicios.

**Ubicación**: `notif_server/urls.py`

**Endpoints**:
- `/api/` - Alert Management Service
- `/auth/` - Authentication Service  
- `/geo/` - Geospatial Service
- `/notifications/` - Notification Service

**Beneficios aplicados**:
- Punto único de entrada para validación de API keys
- Enrutamiento centralizado a microservicios
- Manejo uniforme de errores HTTP

## 2. Circuit Breaker Pattern ✅

**Implementación**: Clase `CircuitBreaker` con instancias para servicios críticos.

**Ubicación**: `utils/circuit_breaker.py`

**Servicios protegidos**:
- `firebase_breaker` - Protege Firebase Cloud Messaging (3 fallos, 30s recovery)
- `websocket_breaker` - Protege WebSocket notifications (5 fallos, 15s recovery)  
- `geospatial_breaker` - Protege cálculos geoespaciales (3 fallos, 20s recovery)

**Fallbacks implementados**:
- Firebase falla → WebSocket como respaldo
- WebSocket falla → Solo almacenamiento en base de datos
- Geospatial falla → Validación básica de coordenadas

**Beneficios aplicados**:
- Previene fallos en cascada
- Mantiene funcionalidad crítica con servicios degradados
- Recuperación automática de servicios

## 3. Database per Service Pattern ✅

**Implementación**: Cada microservicio gestiona sus propias tablas.

**Separación de datos**:
- **Authentication Service**: `auth_service_apikey`
- **Alert Management Service**: `server_notification`
- **Almacenamiento compartido**: Firebase Firestore (para sincronización)

**Beneficios aplicados**:
- Autonomía de datos por servicio
- Escalabilidad independiente
- Aislamiento de cambios de esquema

## 4. Bulkhead Pattern ✅

**Implementación**: Aislamiento de recursos críticos.

**Separaciones implementadas**:
- **Canales de notificación**: Firebase, WebSocket, Webhooks operan independientemente
- **Almacenamiento dual**: SQLite local + Firestore cloud
- **Servicios aislados**: Fallo en autenticación no afecta geolocalización

**Beneficios aplicados**:
- Fallo en un canal no afecta otros
- Redundancia de almacenamiento
- Servicios continúan operando independientemente

## 5. Event-Driven Architecture ✅

**Implementación**: Comunicación asíncrona para notificaciones.

**Componentes**:
- **WebSocket**: `server/consumers.py` - Notificaciones en tiempo real
- **Firebase FCM**: Notificaciones push asíncronas
- **Webhooks**: Integración con sistemas externos

**Beneficios aplicados**:
- Notificaciones en tiempo real < 2s
- Comunicación asíncrona reduce latencia
- Desacoplamiento temporal entre servicios

## Impacto en Requisitos

### Requisitos Funcionales:
- **RF-01 (Envío de alertas)**: Circuit Breaker asegura entrega por canales alternativos
- **RF-02 (Notificaciones multi-canal)**: Bulkhead mantiene canales independientes

### Requisitos No Funcionales:
- **RNF-01 (Disponibilidad 99.9%)**: Circuit Breaker + Bulkhead mantienen servicios críticos
- **RNF-02 (Seguridad)**: API Gateway centraliza validación de API keys
- **RNF-03 (Escalabilidad)**: Database per Service permite escalado independiente
- **RNF-04 (Mantenibilidad)**: Separación de servicios facilita actualizaciones
- **RNF-05 (Tiempo de respuesta < 2s)**: Event-Driven reduce latencia

## Configuración de Circuit Breakers

```python
# Firebase Service
firebase_breaker = CircuitBreaker(
    failure_threshold=3,    # 3 fallos consecutivos
    recovery_timeout=30     # 30 segundos para recuperación
)

# WebSocket Service  
websocket_breaker = CircuitBreaker(
    failure_threshold=5,    # 5 fallos consecutivos
    recovery_timeout=15     # 15 segundos para recuperación
)

# Geospatial Service
geospatial_breaker = CircuitBreaker(
    failure_threshold=3,    # 3 fallos consecutivos
    recovery_timeout=20     # 20 segundos para recuperación
)
```

## Flujo de Tolerancia a Fallos

1. **Solicitud de alerta** → API Gateway
2. **Validación geoespacial** → Circuit Breaker protege, fallback a validación básica
3. **Envío de notificaciones** → Circuit Breaker protege Firebase, fallback a WebSocket
4. **WebSocket falla** → Circuit Breaker protege, fallback a solo base de datos
5. **Almacenamiento** → Dual (SQLite + Firestore) para redundancia

Este conjunto de patrones asegura que el sistema de alertas de emergencia mantenga operatividad crítica incluso ante fallos parciales de servicios.