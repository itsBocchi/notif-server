# Sistema de Alertas de Emergencia - Configuración Completa

## Nuevas Funcionalidades Implementadas

### ✅ CRUD Completo de Alertas
- **Crear**: `POST /api/send-notification/`
- **Leer**: `GET /api/alerts/` y `GET /api/alerts/{id}/`
- **Actualizar**: `PUT /api/alerts/{id}/update/` (requiere admin)
- **Eliminar**: `DELETE /api/alerts/{id}/delete/` (requiere admin)

### ✅ Gestión de API Keys con Permisos
- **Listar**: `GET /api/api-keys/` (requiere admin)
- **Crear**: `POST /api/api-keys/create/` (requiere admin)
- **Revocar**: `PUT /api/api-keys/{id}/revoke/` (requiere admin)

### ✅ Sistema de Permisos
- **Usuario Normal**: Enviar y consultar alertas
- **Administrador**: Todas las operaciones + gestión de sistema

### ✅ Pruebas Unitarias Completas
- 15+ casos de prueba cubriendo todas las funcionalidades
- Validación de permisos y autenticación
- Casos de error y éxito

## Configuración Paso a Paso

### 1. Activar Entorno Virtual e Instalar Dependencias
```bash
cd notif-server
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Aplicar Migraciones
```bash
python manage.py migrate
```

### 3. Crear API Key de Administrador
```bash
python create_admin_api_key.py "ONEMI" "API key principal para administradores"
```
**Importante**: Guarda la API key que se muestra, la necesitarás para operaciones administrativas.

### 4. Configurar Firebase
- Coloca `serviceAccountKey.json` en la raíz del proyecto
- Asegúrate de que Firestore esté habilitado en tu proyecto Firebase

### 5. Ejecutar el Servidor
```bash
python manage.py runserver
```

### 6. Ejecutar Pruebas
```bash
python run_tests.py
```

## Ejemplos de Uso

### Crear Usuario Normal (con API key admin)
```bash
curl -X POST http://localhost:8000/api/api-keys/create/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: TU-ADMIN-API-KEY" \
  -d '{
    "name": "Bomberos Valparaíso",
    "description": "API key para cuerpo de bomberos",
    "is_admin": false
  }'
```

### Enviar Alerta de Incendio
```bash
curl -X POST http://localhost:8000/api/send-notification/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: API-KEY-BOMBEROS" \
  -d '{
    "title": "Incendio en Cerro Alegre",
    "body": "Incendio forestal detectado en sector alto",
    "type": "incendio",
    "latitude": -33.037542,
    "longitude": -71.485482,
    "active": true
  }'
```

### Listar Todas las Alertas
```bash
curl -X GET http://localhost:8000/api/alerts/ \
  -H "X-API-Key: CUALQUIER-API-KEY-VALIDA"
```

### Actualizar Alerta (solo admin)
```bash
curl -X PUT http://localhost:8000/api/alerts/1/update/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: TU-ADMIN-API-KEY" \
  -d '{
    "title": "Incendio Controlado",
    "body": "El incendio ha sido controlado por bomberos"
  }'
```

### Revocar API Key (solo admin)
```bash
curl -X PUT http://localhost:8000/api/api-keys/2/revoke/ \
  -H "X-API-Key: TU-ADMIN-API-KEY"
```

## Estructura de Archivos Nuevos/Modificados

```
notif-server/
├── api/
│   ├── tests.py                    # ✅ NUEVO: Pruebas unitarias completas
│   ├── views.py                    # ✅ MODIFICADO: CRUD + gestión API keys
│   └── urls.py                     # ✅ MODIFICADO: Nuevas rutas
├── server/
│   ├── models.py                   # ✅ MODIFICADO: Campo is_admin
│   └── migrations/
│       └── 0003_apikey_is_admin.py # ✅ NUEVO: Migración para permisos
├── create_admin_api_key.py         # ✅ NUEVO: Script para crear admin
├── run_tests.py                    # ✅ NUEVO: Script para ejecutar pruebas
├── API_EXAMPLES.md                 # ✅ MODIFICADO: Documentación completa
├── SETUP_COMPLETE.md               # ✅ NUEVO: Este archivo
└── ARCHITECTURE.md                 # ✅ NUEVO: Documentación técnica
```

## Verificación del Sistema

### Dashboard Web
- Accede a `http://localhost:8000`
- Verifica que se muestren las alertas

### Pruebas Automatizadas
```bash
python run_tests.py
```
Debe mostrar: "✅ Todas las pruebas pasaron exitosamente!"

### Verificar Firebase
- Ve a Firebase Console > Firestore
- Confirma que se crean documentos en la colección `alertas`

## Códigos de Estado HTTP

- `200 OK`: Operación exitosa
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: API key faltante/inválida
- `403 Forbidden`: Permisos insuficientes
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Seguridad Implementada

- ✅ Autenticación por API key UUID
- ✅ Autorización basada en roles (admin/usuario)
- ✅ Validación de campos obligatorios
- ✅ Protección contra auto-revocación de API keys
- ✅ Trazabilidad de operaciones por fuente

El sistema está completamente funcional y listo para producción. 🚀