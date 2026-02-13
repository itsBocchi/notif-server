from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
from .services import GeospatialService


def validate_request_with_auth_service(request):
    """
    Valida la petición con el servicio de autenticación
    """
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return None, JsonResponse({'error': 'API key is required'}, status=401)
    
    try:
        # En un entorno real, esto sería una llamada HTTP al auth service
        # Por ahora, importamos directamente
        from auth_service.views import authenticate_api_key
        return authenticate_api_key(request)
    except Exception as e:
        return None, JsonResponse({'error': 'Authentication service unavailable'}, status=503)


@csrf_exempt
@require_http_methods(["POST"])
def validate_coordinates(request):
    """
    Endpoint para validar coordenadas geográficas
    """
    api_key_obj, error_response = validate_request_with_auth_service(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return JsonResponse({
                'error': 'Latitude and longitude are required'
            }, status=400)
        
        result = GeospatialService.validate_coordinates(latitude, longitude)
        
        if result['valid']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def calculate_evacuation_zone(request):
    """
    Endpoint para calcular zona completa de evacuación
    """
    api_key_obj, error_response = validate_request_with_auth_service(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        emergency_type = data.get('emergency_type', 'general')
        magnitude = data.get('magnitude')
        
        if latitude is None or longitude is None:
            return JsonResponse({
                'error': 'Latitude and longitude are required'
            }, status=400)
        
        result = GeospatialService.calculate_evacuation_zone(
            latitude, longitude, emergency_type, magnitude
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def calculate_evacuation_radius(request):
    """
    Endpoint para calcular radio de evacuación
    """
    api_key_obj, error_response = validate_request_with_auth_service(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        emergency_type = data.get('emergency_type', 'general')
        magnitude = data.get('magnitude')
        
        result = GeospatialService.calculate_evacuation_radius(emergency_type, magnitude)
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def find_evacuation_points(request):
    """
    Endpoint para encontrar puntos de evacuación
    """
    api_key_obj, error_response = validate_request_with_auth_service(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        emergency_type = data.get('emergency_type', 'general')
        radius = data.get('radius', 500)
        
        if latitude is None or longitude is None:
            return JsonResponse({
                'error': 'Latitude and longitude are required'
            }, status=400)
        
        result = GeospatialService.find_evacuation_points(
            latitude, longitude, emergency_type, radius
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)