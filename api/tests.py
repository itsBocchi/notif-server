from django.test import TestCase, Client
from django.urls import reverse
from auth_service.models import ApiKey
from server.models import Notification
import json
import uuid


class ApiTestCase(TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.client = Client()
        
        # Crear API key normal
        self.normal_api_key = ApiKey.objects.create(
            name="Test Organization",
            description="API key for testing",
            is_admin=False
        )
        
        # Crear API key admin
        self.admin_api_key = ApiKey.objects.create(
            name="Admin Organization", 
            description="Admin API key for testing",
            is_admin=True
        )
        
        # Crear una notificación de prueba
        self.test_notification = Notification.objects.create(
            title="Test Alert",
            body="This is a test alert",
            topic="test",
            source="Test Organization"
        )

    def test_send_notification_success(self):
        """Prueba envío exitoso de notificación"""
        data = {
            "title": "Test Fire Alert",
            "body": "Fire detected in test area",
            "type": "incendio",
            "latitude": -33.037542,
            "longitude": -71.485482,
            "active": True
        }
        
        response = self.client.post(
            reverse('send_notification'),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['alert_type'], 'incendio')

    def test_send_notification_without_api_key(self):
        """Prueba envío sin API key"""
        data = {
            "title": "Test Alert",
            "body": "Test body",
            "type": "general"
        }
        
        response = self.client.post(
            reverse('send_notification'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'API key is required')

    def test_send_notification_invalid_api_key(self):
        """Prueba envío con API key inválida"""
        data = {
            "title": "Test Alert",
            "body": "Test body"
        }
        
        response = self.client.post(
            reverse('send_notification'),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(uuid.uuid4())
        )
        
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Invalid API key')

    def test_send_earthquake_notification(self):
        """Prueba envío de alerta de terremoto"""
        data = {
            "title": "Earthquake Alert",
            "body": "Earthquake detected",
            "type": "earthquake",
            "latitude": -33.050708,
            "longitude": -71.435072,
            "magnitude": 7.5,
            "active": False
        }
        
        response = self.client.post(
            reverse('send_notification'),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['alert_type'], 'earthquake')

    def test_list_alerts_success(self):
        """Prueba listado de alertas"""
        response = self.client.get(
            reverse('list_alerts'),
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('alerts', response_data)
        self.assertGreaterEqual(response_data['count'], 1)

    def test_get_alert_success(self):
        """Prueba obtener alerta específica"""
        response = self.client.get(
            reverse('get_alert', args=[self.test_notification.id]),
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['title'], 'Test Alert')

    def test_update_alert_admin_required(self):
        """Prueba que actualizar alerta requiere permisos de admin"""
        data = {"title": "Updated Title"}
        
        # Con API key normal (debería fallar)
        response = self.client.put(
            reverse('update_alert', args=[self.test_notification.id]),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 403)

    def test_update_alert_admin_success(self):
        """Prueba actualización exitosa con permisos de admin"""
        data = {"title": "Updated Title"}
        
        response = self.client.put(
            reverse('update_alert', args=[self.test_notification.id]),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(self.admin_api_key.key)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_delete_alert_admin_required(self):
        """Prueba que eliminar alerta requiere permisos de admin"""
        # Con API key normal (debería fallar)
        response = self.client.delete(
            reverse('delete_alert', args=[self.test_notification.id]),
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 403)

    def test_create_api_key_admin_required(self):
        """Prueba que crear API key requiere permisos de admin"""
        data = {
            "name": "New Organization",
            "description": "New API key",
            "is_admin": False
        }
        
        # Con API key normal (debería fallar)
        response = self.client.post(
            reverse('create_api_key'),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 403)

    def test_create_api_key_admin_success(self):
        """Prueba creación exitosa de API key con permisos de admin"""
        data = {
            "name": "New Organization",
            "description": "New API key",
            "is_admin": False
        }
        
        response = self.client.post(
            reverse('create_api_key'),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(self.admin_api_key.key)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertIn('api_key', response_data)

    def test_list_api_keys_admin_required(self):
        """Prueba que listar API keys requiere permisos de admin"""
        response = self.client.get(
            reverse('list_api_keys'),
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 403)

    def test_list_api_keys_admin_success(self):
        """Prueba listado exitoso de API keys con permisos de admin"""
        response = self.client.get(
            reverse('list_api_keys'),
            HTTP_X_API_KEY=str(self.admin_api_key.key)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('api_keys', response_data)
        self.assertGreaterEqual(response_data['count'], 2)

    def test_revoke_api_key_admin_success(self):
        """Prueba revocación exitosa de API key"""
        # Crear una API key adicional para revocar
        target_key = ApiKey.objects.create(
            name="Target Organization",
            description="Key to be revoked"
        )
        
        response = self.client.put(
            reverse('revoke_api_key', args=[target_key.id]),
            HTTP_X_API_KEY=str(self.admin_api_key.key)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        # Verificar que la key fue desactivada
        target_key.refresh_from_db()
        self.assertFalse(target_key.is_active)

    def test_revoke_own_api_key_forbidden(self):
        """Prueba que no se puede revocar la propia API key"""
        response = self.client.put(
            reverse('revoke_api_key', args=[self.admin_api_key.id]),
            HTTP_X_API_KEY=str(self.admin_api_key.key)
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Cannot revoke your own API key')

    def test_missing_required_fields(self):
        """Prueba validación de campos requeridos"""
        data = {"body": "Missing title"}
        
        response = self.client.post(
            reverse('send_notification'),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Title and body are required')

    def test_missing_coordinates_for_emergency(self):
        """Prueba validación de coordenadas para alertas de emergencia"""
        data = {
            "title": "Emergency Alert",
            "body": "Emergency without coordinates",
            "type": "incendio"
        }
        
        response = self.client.post(
            reverse('send_notification'),
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_API_KEY=str(self.normal_api_key.key)
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Latitude and longitude are required for emergency alerts')