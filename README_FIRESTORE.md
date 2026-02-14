# Integración con Firebase Firestore para Alertas de Catástrofe

Este sistema está configurado para guardar alertas de catástrofe en la colección "alertas" de Firebase Firestore con formatos específicos según el tipo de alerta.

## Configuración

1. El archivo de credenciales de Firebase debe estar en la raíz del proyecto con el nombre `serviceAccountKey.json`
2. El sistema detectará automáticamente este archivo e inicializará Firebase con estas credenciales

## Tipos de Alertas de Catástrofe

### 1. Alertas de Incendio

Las alertas de incendio se guardan con el siguiente formato:

```javascript
{
  activo: true,
  puntos_evacuacion: [
    { latitude: -33.037542, longitude: -71.485482 }
  ],
  radios_evacuacion: [1], // 1 metro
  time: Timestamp.fromDate(new Date("2024-11-28T18:05:54-03:00")),
  title: "USM Sede Viña del Mar",
  type: "incendio"
}
```

### 2. Alertas de Terremoto

Las alertas de terremoto se guardan con el siguiente formato:

```javascript
{
  activo: false,
  magnitude: 7.5, // Solo en terremotos
  puntos_evacuacion: [
    { latitude: -33.050708, longitude: -71.435072 }
  ],
  radios_evacuacion: [500], // 500 metros
  time: Timestamp.fromDate(new Date("2024-11-15T08:04:45-03:00")),
  title: "Quilpué, Chile",
  type: "earthquake"
}
```

## Envío de Alertas

### Usando la API

Para enviar una alerta de incendio:

```bash
curl -X POST http://localhost:8000/api/send-notification/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key" \
  -d '{
    "title": "USM Sede Viña del Mar",
    "body": "Incendio detectado en el campus",
    "topic": "incendio",
    "type": "incendio",
    "latitude": -33.03754238598971,
    "longitude": -71.48548225923,
    "active": true
  }'
```

Para enviar una alerta de terremoto:

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

### Usando los Scripts de Prueba

Para probar alertas de incendio:

```bash
python test_fire_alert.py <api_key> "USM Sede Viña del Mar" "Incendio detectado" -33.03754238598971 -71.48548225923 true
```

Para probar alertas de terremoto:

```bash
python test_earthquake_alert.py <api_key> "Quilpué, Chile" "Terremoto de magnitud 7.5" 7.5 -33.050708 -71.435072 false
```