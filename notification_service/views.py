from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .services import NotificationDeliveryService


def validate_request_with_auth_service(request):
    """
    Valida la petición con el servicio de autenticación
    """
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return None, JsonResponse({'error': 'API key is required'}, status=401)
    
    try:
        from auth_service.views import authenticate_api_key
        return authenticate_api_key(request)
    except Exception as e:
        return None, JsonResponse({'error': 'Authentication service unavailable'}, status=503)


@csrf_exempt
@require_http_methods(["POST"])
def send_notification(request):
    """
    Endpoint para enviar notificación por un canal específico
    """
    api_key_obj, error_response = validate_request_with_auth_service(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        title = data.get('title')
        body = data.get('body')
        channel = data.get('channel', 'firebase')
        
        if not title or not body:
            return JsonResponse({
                'error': 'Title and body are required'
            }, status=400)
        
        if channel == 'firebase':
            topic = data.get('topic', 'general')
            notification_data = data.get('data', {})
            result = NotificationDeliveryService.send_firebase_notification(
                title, body, topic, notification_data
            )
        elif channel == 'websocket':
            group_name = data.get('group', 'notifications')
            message = {
                'title': title,
                'body': body,
                'source': api_key_obj.name,
                **data.get('data', {})
            }
            result = NotificationDeliveryService.send_websocket_notification(
                group_name, message
            )
        elif channel == 'webhook':
            webhook_urls = data.get('webhook_urls', [])
            payload = {
                'title': title,
                'body': body,
                'source': api_key_obj.name,
                **data.get('data', {})
            }
            result = NotificationDeliveryService.send_webhook_notification(
                webhook_urls, payload
            )
        else:
            return JsonResponse({
                'error': f'Unsupported channel: {channel}'
            }, status=400)
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def broadcast_notification(request):
    """
    Endpoint para enviar notificación por múltiples canales
    """
    api_key_obj, error_response = validate_request_with_auth_service(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        title = data.get('title')
        body = data.get('body')
        channels = data.get('channels', {})
        
        if not title or not body:
            return JsonResponse({
                'error': 'Title and body are required'
            }, status=400)
        
        if not channels:
            return JsonResponse({
                'error': 'At least one channel configuration is required'
            }, status=400)
        
        result = NotificationDeliveryService.send_multi_channel_notification(
            title, body, channels
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_firebase_notification(request):
    """
    Endpoint específico para Firebase Cloud Messaging
    """
    api_key_obj, error_response = validate_request_with_auth_service(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        title = data.get('title')
        body = data.get('body')
        topic = data.get('topic', 'general')
        notification_data = data.get('data', {})
        
        if not title or not body:
            return JsonResponse({
                'error': 'Title and body are required'
            }, status=400)
        
        result = NotificationDeliveryService.send_firebase_notification(
            title, body, topic, notification_data
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_websocket_notification(request):
    """
    Endpoint específico para WebSocket
    """
    api_key_obj, error_response = validate_request_with_auth_service(request)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        title = data.get('title')
        body = data.get('body')
        group_name = data.get('group', 'notifications')
        
        if not title or not body:
            return JsonResponse({
                'error': 'Title and body are required'
            }, status=400)
        
        message = {
            'title': title,
            'body': body,
            'source': api_key_obj.name,
            **data.get('data', {})
        }
        
        result = NotificationDeliveryService.send_websocket_notification(
            group_name, message
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)