from django.test import TestCase
from auth_service.models import ApiKey
from server.models import Notification
from unittest.mock import patch

class PersistenceTestCase(TestCase):
    
    def setUp(self):
        self.api_key = ApiKey.objects.create(
            name="Test Key",
            entidad="Test Organization",
            is_active=True
        )
    
    def test_local_database_save(self):
        """Prueba guardado en base de datos local"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Local DB Test',
            'body': 'Testing local persistence',
            'type': 'incendio',
            'latitude': -33.0,
            'longitude': -71.0,
            'active': True
        }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se guardó en la base de datos local
        notification = Notification.objects.get(title='Local DB Test')
        self.assertEqual(notification.emergency_type, 'incendio')
        self.assertEqual(notification.latitude, -33.0)
        self.assertEqual(notification.longitude, -71.0)
        self.assertTrue(notification.active)
        self.assertEqual(notification.source, 'Test Organization')
    
    def test_earthquake_data_persistence(self):
        """Prueba persistencia de datos de terremoto"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Earthquake Persistence Test',
            'body': 'Testing earthquake data',
            'type': 'earthquake',
            'latitude': -33.050708,
            'longitude': -71.435072,
            'magnitude': 6.8,
            'active': False
        }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar datos específicos de terremoto
        notification = Notification.objects.get(title='Earthquake Persistence Test')
        self.assertEqual(notification.emergency_type, 'earthquake')
        self.assertEqual(notification.magnitude, 6.8)
        self.assertFalse(notification.active)
    
    @patch('firebase_utils.save_fire_alert')
    def test_firebase_failure_fallback(self, mock_firebase):
        """Prueba que el sistema funcione aunque Firebase falle"""
        mock_firebase.return_value = False  # Simular fallo de Firebase
        
        response = self.client.post('/api/send-notification/', {
            'title': 'Firebase Failure Test',
            'body': 'Testing Firebase failure handling',
            'type': 'incendio',
            'latitude': -33.0,
            'longitude': -71.0,
            'active': True
        }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
        
        # El sistema debe seguir funcionando
        self.assertEqual(response.status_code, 200)
        
        # Debe guardarse localmente aunque Firebase falle
        self.assertTrue(Notification.objects.filter(title='Firebase Failure Test').exists())
    
    def test_data_integrity(self):
        """Prueba integridad de datos"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Data Integrity Test',
            'body': 'Testing data integrity',
            'type': 'incendio',
            'latitude': -33.037542,
            'longitude': -71.485482,
            'active': True
        }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar que todos los campos se guardaron correctamente
        notification = Notification.objects.get(title='Data Integrity Test')
        self.assertIsNotNone(notification.created_at)
        self.assertEqual(notification.api_key, self.api_key)
        self.assertEqual(notification.source, self.api_key.entidad)