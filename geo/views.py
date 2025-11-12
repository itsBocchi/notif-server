from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import math
from server.models import ApiKey

def check_api_key(request):
    """Helper para verificar API key válida"""
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return None, JsonResponse({'error': 'API key is required'}, status=401)
    
    try:
        api_key_obj = ApiKey.objects.get(key=api_key, is_active=True)
        return api_key_obj, None
    except (ApiKey.DoesNotExist, ValueError):
        return None, JsonResponse({'error': 'Invalid API key'}, status=401)

@csrf_exempt
def validate_coordinates(request):
    """
    Valida coordenadas geográficas
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    api_key_obj, error_response = check_api_key(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
        
        # Validar rangos
        if not (-90 <= latitude <= 90):
            return JsonResponse({
                'valid': False,
                'error': 'Latitude must be between -90 and 90',
                'latitude': latitude
            })
        
        if not (-180 <= longitude <= 180):
            return JsonResponse({
                'valid': False,
                'error': 'Longitude must be between -180 and 180',
                'longitude': longitude
            })
        
        # Determinar si está en Chile (aproximado)
        in_chile = (-56 <= latitude <= -17) and (-109 <= longitude <= -66)
        
        return JsonResponse({
            'valid': True,
            'latitude': latitude,
            'longitude': longitude,
            'in_chile': in_chile,
            'validated_by': api_key_obj.name
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def calculate_evacuation_zone(request):
    """
    Calcula zona de evacuación basada en tipo de emergencia
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    api_key_obj, error_response = check_api_key(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        emergency_type = data.get('emergency_type')
        magnitude = data.get('magnitude')
        
        if latitude is None or longitude is None or not emergency_type:
            return JsonResponse({'error': 'Latitude, longitude and emergency_type are required'}, status=400)
        
        # Calcular radio según tipo de emergencia
        if emergency_type == 'incendio':
            radius_meters = 1000  # 1km para incendios
            evacuation_time = 15  # 15 minutos
        elif emergency_type == 'earthquake':
            # Radio basado en magnitud
            mag = magnitude or 7.0
            radius_meters = int(mag * 100)  # 100m por grado de magnitud
            evacuation_time = int(mag * 2)  # 2 minutos por grado
        else:
            radius_meters = 500  # Default 500m
            evacuation_time = 10
        
        # Calcular coordenadas del perímetro (círculo simple)
        perimeter_points = []
        for angle in range(0, 360, 30):  # Cada 30 grados
            rad = math.radians(angle)
            # Aproximación simple para coordenadas
            lat_offset = (radius_meters / 111000) * math.cos(rad)
            lon_offset = (radius_meters / (111000 * math.cos(math.radians(latitude)))) * math.sin(rad)
            
            perimeter_points.append({
                'latitude': latitude + lat_offset,
                'longitude': longitude + lon_offset
            })
        
        return JsonResponse({
            'center': {'latitude': latitude, 'longitude': longitude},
            'emergency_type': emergency_type,
            'radius_meters': radius_meters,
            'evacuation_time_minutes': evacuation_time,
            'perimeter_points': perimeter_points,
            'calculated_by': api_key_obj.name
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def calculate_evacuation_radius(request):
    """
    Calcula radio de evacuación óptimo
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    api_key_obj, error_response = check_api_key(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        emergency_type = data.get('emergency_type')
        magnitude = data.get('magnitude')
        population_density = data.get('population_density', 'medium')
        
        if not emergency_type:
            return JsonResponse({'error': 'emergency_type is required'}, status=400)
        
        # Calcular radio base
        if emergency_type == 'incendio':
            base_radius = 1000
        elif emergency_type == 'earthquake':
            mag = magnitude or 7.0
            base_radius = int(mag * 150)
        else:
            base_radius = 500
        
        # Ajustar por densidad poblacional
        density_multiplier = {
            'low': 0.7,
            'medium': 1.0,
            'high': 1.5,
            'very_high': 2.0
        }.get(population_density, 1.0)
        
        final_radius = int(base_radius * density_multiplier)
        
        return JsonResponse({
            'emergency_type': emergency_type,
            'magnitude': magnitude,
            'population_density': population_density,
            'base_radius_meters': base_radius,
            'density_multiplier': density_multiplier,
            'recommended_radius_meters': final_radius,
            'calculated_by': api_key_obj.name
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def find_evacuation_points(request):
    """
    Encuentra puntos de evacuación cercanos
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    api_key_obj, error_response = check_api_key(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius_km = data.get('radius_km', 5)
        
        if latitude is None or longitude is None:
            return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
        
        # Puntos de evacuación simulados para la región de Valparaíso
        evacuation_points = [
            {
                'id': 1,
                'name': 'Estadio Municipal de Viña del Mar',
                'type': 'stadium',
                'latitude': -33.0245,
                'longitude': -71.5518,
                'capacity': 5000,
                'distance_km': 2.1
            },
            {
                'id': 2,
                'name': 'Plaza Victoria',
                'type': 'plaza',
                'latitude': -33.0458,
                'longitude': -71.6197,
                'capacity': 2000,
                'distance_km': 1.8
            },
            {
                'id': 3,
                'name': 'Campus USM',
                'type': 'university',
                'latitude': -33.0375,
                'longitude': -71.4855,
                'capacity': 3000,
                'distance_km': 0.5
            },
            {
                'id': 4,
                'name': 'Hospital Gustavo Fricke',
                'type': 'hospital',
                'latitude': -33.0472,
                'longitude': -71.6127,
                'capacity': 1000,
                'distance_km': 3.2
            }
        ]
        
        # Filtrar por radio
        nearby_points = [
            point for point in evacuation_points 
            if point['distance_km'] <= radius_km
        ]
        
        # Ordenar por distancia
        nearby_points.sort(key=lambda x: x['distance_km'])
        
        return JsonResponse({
            'search_center': {'latitude': latitude, 'longitude': longitude},
            'search_radius_km': radius_km,
            'evacuation_points': nearby_points,
            'total_found': len(nearby_points),
            'total_capacity': sum(point['capacity'] for point in nearby_points),
            'searched_by': api_key_obj.name
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)