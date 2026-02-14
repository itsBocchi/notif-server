# Endpoints Implementados - Sistema de Alertas de Emergencia

## Tabla de Endpoints Públicos

| Endpoint | Método | Permisos | Caso de Uso | Descripción |
|----------|--------|----------|-------------|-------------|
| /api/send-notification/ | POST | User/Admin | CU-01 | Crear y enviar alerta de emergencia |
| /api/notifications/ | GET | User/Admin | CU-02 | Consultar alertas existentes |

## Servicios Internos (No Expuestos Públicamente)

| Servicio | Función | Caso de Uso | Descripción |
|----------|---------|-------------|-------------|
| Auth Service | validate_api_key() | CU-10 | Validación interna de credenciales |
| Alert Service | create_notification() | CU-01 | Procesamiento interno de alertas |
| Alert Service | get_notifications() | CU-02 | Consulta interna de base de datos |
| Notification Service | send_alert() | CU-09 | Sincronización con Firebase |
| Geospatial Service | process_coordinates() | CU-05 | Procesamiento interno de coordenadas |

## Acceso Directo Firebase (Sin API Backend)

| Recurso | Método | Permisos | Caso de Uso | Descripción |
|---------|--------|----------|-------------|-------------|
| Firestore /alerts | READ | Público | CU-04, CU-05 | Consulta directa desde apps móviles |

## Autenticación

- **Header requerido**: `X-API-Key: <uuid>`
- **Niveles de permisos**: User, Admin
- **Validación**: Automática en todos los endpoints públicos

## Notas de Implementación

- **MVP Funcional**: Solo endpoints esenciales implementados
- **Arquitectura Modular**: Servicios internos preparados para extensión
- **Acceso Híbrido**: API REST para organismos + acceso directo Firebase para móviles
- **Tolerancia a Fallos**: Circuit Breaker implementado en servicios internos
- **Escalabilidad**: Arquitectura preparada para agregar endpoints futuros

## Casos de Uso No Implementados Públicamente

Los siguientes casos de uso están implementados como **funcionalidad interna** pero no expuestos como endpoints públicos:

- **CU-03**: Ver Historial (funcionalidad incluida en CU-02)
- **CU-06**: Gestionar API Keys (administración manual)
- **CU-07**: Monitorear Sistema (logs internos)
- **CU-08**: Configurar Notificaciones (configuración estática)