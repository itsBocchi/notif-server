import math
from typing import Dict, List, Tuple, Optional


class GeospatialService:
    """
    Servicio especializado en cálculos geoespaciales para emergencias
    Microservicio: Geospatial Processing Service
    """
    
    # Radios por defecto por tipo de emergencia (en metros)
    DEFAULT_RADII = {
        'incendio': 1,
        'earthquake': 500,
        'tsunami': 2000,
        'avalancha': 1500
    }
    
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> Dict:
        """
        Valida coordenadas geográficas
        
        Args:
            latitude: Latitud en grados decimales
            longitude: Longitud en grados decimales
            
        Returns:
            Dict con resultado de validación
        """
        try:
            lat = float(latitude)
            lng = float(longitude)
            
            if not (-90 <= lat <= 90):
                return {
                    'valid': False,
                    'error': 'Latitude must be between -90 and 90 degrees'
                }
            
            if not (-180 <= lng <= 180):
                return {
                    'valid': False,
                    'error': 'Longitude must be between -180 and 180 degrees'
                }
            
            return {
                'valid': True,
                'coordinates': {
                    'latitude': lat,
                    'longitude': lng
                }
            }
            
        except (ValueError, TypeError):
            return {
                'valid': False,
                'error': 'Invalid coordinate format'
            }
    
    @staticmethod
    def calculate_evacuation_radius(emergency_type: str, magnitude: Optional[float] = None) -> Dict:
        """
        Calcula el radio de evacuación según el tipo de emergencia
        
        Args:
            emergency_type: Tipo de emergencia
            magnitude: Magnitud del evento (para terremotos)
            
        Returns:
            Dict con radio calculado
        """
        try:
            base_radius = GeospatialService.DEFAULT_RADII.get(emergency_type, 500)
            
            # Ajuste dinámico para terremotos según magnitud
            if emergency_type == 'earthquake' and magnitude:
                if magnitude >= 8.0:
                    radius = 2000
                elif magnitude >= 7.0:
                    radius = 1000
                elif magnitude >= 6.0:
                    radius = 500
                else:
                    radius = 200
            else:
                radius = base_radius
            
            return {
                'success': True,
                'radius_meters': radius,
                'emergency_type': emergency_type,
                'magnitude': magnitude
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calcula distancia entre dos puntos usando fórmula de Haversine
        
        Returns:
            Distancia en metros
        """
        R = 6371000  # Radio de la Tierra en metros
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    @staticmethod
    def find_evacuation_points(latitude: float, longitude: float, 
                             emergency_type: str, radius: int) -> Dict:
        """
        Encuentra puntos de evacuación seguros
        
        Args:
            latitude: Latitud del evento
            longitude: Longitud del evento
            emergency_type: Tipo de emergencia
            radius: Radio de evacuación en metros
            
        Returns:
            Dict con puntos de evacuación
        """
        try:
            # Cálculo básico de puntos de evacuación
            # En una implementación real, esto consultaría una base de datos
            # de refugios, hospitales, etc.
            
            evacuation_points = []
            
            # Generar puntos en las 4 direcciones cardinales
            # fuera del radio de peligro
            safe_distance = radius * 1.5  # 50% más lejos del radio de peligro
            
            # Conversión aproximada: 1 grado ≈ 111,000 metros
            lat_offset = safe_distance / 111000
            lng_offset = safe_distance / (111000 * math.cos(math.radians(latitude)))
            
            directions = [
                ('Norte', latitude + lat_offset, longitude),
                ('Sur', latitude - lat_offset, longitude),
                ('Este', latitude, longitude + lng_offset),
                ('Oeste', latitude, longitude - lng_offset)
            ]
            
            for direction, lat, lng in directions:
                evacuation_points.append({
                    'direction': direction,
                    'latitude': lat,
                    'longitude': lng,
                    'distance_from_event': safe_distance,
                    'type': 'calculated_safe_point'
                })
            
            return {
                'success': True,
                'evacuation_points': evacuation_points,
                'total_points': len(evacuation_points),
                'safe_distance_meters': safe_distance
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def calculate_evacuation_zone(latitude: float, longitude: float, 
                                emergency_type: str, magnitude: Optional[float] = None) -> Dict:
        """
        Calcula zona completa de evacuación
        
        Returns:
            Dict con información completa de la zona
        """
        try:
            # Validar coordenadas
            coord_validation = GeospatialService.validate_coordinates(latitude, longitude)
            if not coord_validation['valid']:
                return coord_validation
            
            # Calcular radio
            radius_info = GeospatialService.calculate_evacuation_radius(emergency_type, magnitude)
            if not radius_info['success']:
                return radius_info
            
            radius = radius_info['radius_meters']
            
            # Encontrar puntos de evacuación
            evacuation_info = GeospatialService.find_evacuation_points(
                latitude, longitude, emergency_type, radius
            )
            
            if not evacuation_info['success']:
                return evacuation_info
            
            return {
                'success': True,
                'event_location': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'emergency_type': emergency_type,
                'magnitude': magnitude,
                'evacuation_radius_meters': radius,
                'evacuation_points': evacuation_info['evacuation_points'],
                'safe_distance_meters': evacuation_info['safe_distance_meters']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }