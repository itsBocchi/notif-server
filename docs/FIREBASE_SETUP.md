# Configuración de Firebase Cloud Messaging

Para habilitar el envío de notificaciones a dispositivos móviles, necesitas configurar Firebase Cloud Messaging (FCM).

## Pasos para configurar Firebase

1. **Crear un proyecto en Firebase Console**
   - Ve a [Firebase Console](https://console.firebase.google.com/)
   - Haz clic en "Añadir proyecto"
   - Sigue los pasos para crear un nuevo proyecto

2. **Obtener credenciales de servicio**
   - En la consola de Firebase, ve a Configuración del proyecto > Cuentas de servicio
   - Haz clic en "Generar nueva clave privada"
   - Descarga el archivo JSON de credenciales

3. **Configurar el proyecto**
   - Coloca el archivo JSON descargado en la raíz del proyecto
   - Renómbralo a `serviceAccountKey.json` o actualiza la variable de entorno `FIREBASE_CREDENTIALS_PATH` en el archivo `.env`

4. **Verificar la configuración**
   - Reinicia el servidor Django
   - Deberías ver el mensaje "Firebase initialized successfully with credentials from serviceAccountKey.json"

## Modo simulado

Si no configuras las credenciales de Firebase, el sistema funcionará en modo simulado:
- Las notificaciones se mostrarán en la interfaz web
- Se guardarán en la base de datos
- Pero NO se enviarán a dispositivos móviles

## Estructura del archivo de credenciales

El archivo JSON de credenciales debe tener una estructura similar a esta:

```json
{
  "type": "service_account",
  "project_id": "tu-proyecto-id",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxx@tu-proyecto-id.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxx%40tu-proyecto-id.iam.gserviceaccount.com"
}
```