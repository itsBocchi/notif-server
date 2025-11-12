from django.test import TestCase
from auth_service.models import ApiKey

class ValidationTestCase(TestCase):
    
    def setUp(self):
        self.api_key = ApiKey.objects.create(
            name="Test Key",
            entidad="Test Org",
            is_active=True
        )
    
    def test_missing_title(self):
        """Prueba título faltante"""
        response = self.client.post('/api/send-notification/', {
            'body': 'Test body',
            'type': 'incendio'
        }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
        
        self.assertEqual(response.status_code, 400)
    
    def test_missing_body(self):
        """Prueba cuerpo faltante"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Test title',
            'type': 'incendio'
        }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
        
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_coordinates(self):
        """Prueba coordenadas inválidas"""
        invalid_coords = [
            {'latitude': 91.0, 'longitude': -71.0},   # Lat > 90
            {'latitude': -91.0, 'longitude': -71.0},  # Lat < -90
            {'latitude': -33.0, 'longitude': 181.0},  # Lon > 180
            {'latitude': -33.0, 'longitude': -181.0}  # Lon < -180
        ]
        
        for coords in invalid_coords:
            response = self.client.post('/api/send-notification/', {
                'title': 'Test',
                'body': 'Test',
                'type': 'incendio',
                **coords
            }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
            
            # Debería rechazar coordenadas inválidas
            self.assertIn(response.status_code, [400, 422])
    
    def test_valid_alert_types(self):
        """Prueba tipos de alerta válidos"""
        valid_types = ['incendio', 'earthquake', 'general']
        
        for alert_type in valid_types:
            response = self.client.post('/api/send-notification/', {
                'title': f'Test {alert_type}',
                'body': 'Test body',
                'type': alert_type,
                'latitude': -33.0,
                'longitude': -71.0
            }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
            
            self.assertEqual(response.status_code, 200)
    
    def test_earthquake_magnitude_validation(self):
        """Prueba validación de magnitud para terremotos"""
        response = self.client.post('/api/send-notification/', {
            'title': 'Earthquake Test',
            'body': 'Test earthquake',
            'type': 'earthquake',
            'latitude': -33.0,
            'longitude': -71.0,
            'magnitude': 7.5
        }, content_type='application/json', HTTP_X_API_KEY=str(self.api_key.key))
        
        self.assertEqual(response.status_code, 200)