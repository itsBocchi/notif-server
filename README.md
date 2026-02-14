# Sistema de Alertas de Catástrofe

API para enviar alertas de catástrofe (incendios y terremotos) con almacenamiento en Firebase Firestore.

## Requisitos

- Python 3.8+
- Django 4.2+
- Firebase Admin SDK
- Archivo de credenciales de Firebase (`serviceAccountKey.json`)

## Instalación

1. Clonar el repositorio e instalar dependencias:
```
git clone https://github.com/yourusername/notif-server.git
cd notif-server
python -m venv venv
venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```

2. Configurar Firebase:
   - Colocar el archivo `serviceAccountKey.json` en la raíz del proyecto

3. Aplicar migraciones y crear una API key:
```
python manage.py migrate
python create_api_key.py "Sistema de Alertas"
```

4. Ejecutar el servidor:
```
python manage.py runserver
```

## Envío de Alertas

### Alerta de Incendio

```bash
python test_fire_alert.py <api_key> "USM Sede Viña del Mar" "Incendio detectado" -33.037542 -71.485482 true
```

### Alerta de Terremoto

```bash
python test_earthquake_alert.py <api_key> "Quilpué, Chile" "Terremoto de magnitud 7.5" 7.5 -33.050708 -71.435072 false
```

## Formato de Datos en Firestore

### Incendio
```javascript
{
  activo: true,
  puntos_evacuacion: [
    { latitude: -33.037542, longitude: -71.485482 }
  ],
  radios_evacuacion: [1], // 1 metro
  time: Timestamp,
  title: "USM Sede Viña del Mar",
  type: "incendio"
}
```

### Terremoto
```javascript
{
  activo: false,
  magnitude: 7.5,
  puntos_evacuacion: [
    { latitude: -33.050708, longitude: -71.435072 }
  ],
  radios_evacuacion: [500], // 500 metros
  time: Timestamp,
  title: "Quilpué, Chile",
  type: "earthquake"
}
```

## API REST

```
POST /api/send-notification/
Content-Type: application/json
X-API-Key: tu-api-key-uuid

{
    "title": "Título de la alerta",
    "body": "Descripción de la alerta",
    "type": "incendio", // o "earthquake"
    "latitude": -33.037542,
    "longitude": -71.485482,
    "magnitude": 7.5, // solo para terremotos
    "active": true
}
```