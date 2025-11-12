from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import json
from .models import ApiKey


def authenticate_api_key(request, require_admin=False):
    """
    Función de autenticación centralizada para el microservicio
    """
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return None, JsonResponse({'error': 'API key is required'}, status=401)
    
    try:
        api_key_obj = ApiKey.objects.get(key=api_key, is_active=True)
        if require_admin and not api_key_obj.is_admin:
            return None, JsonResponse({'error': 'Admin privileges required'}, status=403)
        return api_key_obj, None
    except (ApiKey.DoesNotExist, ValueError):
        return None, JsonResponse({'error': 'Invalid API key'}, status=401)


@csrf_exempt
@require_http_methods(["POST"])
def validate_api_key(request):
    """
    Endpoint para validar API keys desde otros microservicios
    """
    try:
        data = json.loads(request.body)
        api_key = data.get('api_key')
        require_admin = data.get('require_admin', False)
        
        if not api_key:
            return JsonResponse({'valid': False, 'error': 'API key is required'}, status=400)
        
        try:
            api_key_obj = ApiKey.objects.get(key=api_key, is_active=True)
            if require_admin and not api_key_obj.is_admin:
                return JsonResponse({
                    'valid': False, 
                    'error': 'Admin privileges required'
                }, status=403)
            
            return JsonResponse({
                'valid': True,
                'user_info': {
                    'name': api_key_obj.name,
                    'is_admin': api_key_obj.is_admin,
                    'id': api_key_obj.id
                }
            })
        except (ApiKey.DoesNotExist, ValueError):
            return JsonResponse({'valid': False, 'error': 'Invalid API key'}, status=401)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_api_key(request):
    """
    Crear nueva API key (requiere permisos de admin)
    """
    api_key_obj, error_response = authenticate_api_key(request, require_admin=True)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        is_admin = data.get('is_admin', False)
        
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        
        new_api_key = ApiKey.objects.create(
            name=name,
            description=description,
            is_admin=is_admin
        )
        
        return JsonResponse({
            'success': True,
            'message': 'API key created successfully',
            'api_key': str(new_api_key.key),
            'name': new_api_key.name,
            'is_admin': new_api_key.is_admin
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def list_api_keys(request):
    """
    Lista todas las API keys (requiere permisos de admin)
    """
    api_key_obj, error_response = authenticate_api_key(request, require_admin=True)
    if error_response:
        return error_response
    
    try:
        api_keys = ApiKey.objects.all().order_by('-created_at')
        data = [{
            'id': key.id,
            'key': str(key.key),
            'name': key.name,
            'description': key.description,
            'is_active': key.is_active,
            'is_admin': key.is_admin,
            'created_at': key.created_at.isoformat()
        } for key in api_keys]
        
        return JsonResponse({'api_keys': data, 'count': len(data)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def revoke_api_key(request, key_id):
    """
    Revoca (desactiva) una API key (requiere permisos de admin)
    """
    api_key_obj, error_response = authenticate_api_key(request, require_admin=True)
    if error_response:
        return error_response
    
    try:
        target_key = get_object_or_404(ApiKey, id=key_id)
        
        if target_key.id == api_key_obj.id:
            return JsonResponse({'error': 'Cannot revoke your own API key'}, status=400)
        
        target_key.is_active = False
        target_key.save()
        
        return JsonResponse({
            'success': True,
            'message': f'API key for "{target_key.name}" has been revoked'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)