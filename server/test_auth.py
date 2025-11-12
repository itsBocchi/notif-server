from django.test import TestCase
from auth_service.models import ApiKey

class AuthTestCase(TestCase):
    
    def setUp(self):
        self.valid_key = ApiKey.objects.create(
            name="Valid Key",
            entidad="Test Org",
            is_active=True
        )
        self.inactive_key = ApiKey.objects.create(
            name="Inactive Key", 
            entidad="Test Org",
            is_active=False
        )
    
    def test_valid_api_key(self):
        """Prueba API key válida"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Test',
            'body': 'Test',
            'type': 'incendio',
            'latitude': -33.0,
            'longitude': -71.0
        }, content_type='application/json', HTTP_X_API_KEY=str(self.valid_key.key))
        
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_api_key(self):
        """Prueba API key inválida"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Test',
            'body': 'Test',
            'type': 'incendio'
        }, content_type='application/json', HTTP_X_API_KEY='invalid-key')
        
        self.assertEqual(response.status_code, 401)
    
    def test_inactive_api_key(self):
        """Prueba API key inactiva"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Test',
            'body': 'Test',
            'type': 'incendio'
        }, content_type='application/json', HTTP_X_API_KEY=str(self.inactive_key.key))
        
        self.assertEqual(response.status_code, 401)
    
    def test_missing_api_key(self):
        """Prueba sin API key"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Test',
            'body': 'Test',
            'type': 'incendio'
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 401)