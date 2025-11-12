from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import firebase_admin
from firebase_admin import messaging
from server.consumers import NotificationConsumer
from server.models import Notification
from auth_service.models import ApiKey
from firebase_utils import save_fire_alert, save_earthquake_alert

def check_admin_permission(api_key):
    """
    Verifica si la API key tiene permisos de administrador
    """
    try:
        api_key_obj = ApiKey.objects.get(key=api_key, is_active=True)
        if not api_key_obj.is_admin:
            return None, JsonResponse({'error': 'Admin permissions required'}, status=403)
        return api_key_obj, None
    except (ApiKey.DoesNotExist, ValueError):
        return None, JsonResponse({'error': 'Invalid API key'}, status=401)

@csrf_exempt
@require_POST
def send_notification(request):
    """
    API endpoint to send notifications
    Requires API key authentication
    """
    try:
        # Check API key
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return JsonResponse({'error': 'API key is required'}, status=401)
        
        try:
            # Validar formato UUID
            import uuid
            uuid.UUID(api_key)
            api_key_obj = ApiKey.objects.get(key=api_key, is_active=True)
        except (ApiKey.DoesNotExist, ValueError, TypeError):
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        # Parse request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        title = data.get('title')
        body = data.get('body')
        topic = data.get('topic', 'general')
        alert_type = data.get('type', 'general')  # Tipo de alerta: incendio, earthquake, general
        
        # Datos adicionales para alertas específicas
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        magnitude = data.get('magnitude')
        active = data.get('active', True)
        
        if not title or not body:
            return JsonResponse({'error': 'Title and body are required'}, status=400)
        
        # Validar coordenadas si están presentes
        if latitude is not None:
            if not (-90 <= latitude <= 90):
                return JsonResponse({'error': 'Latitude must be between -90 and 90'}, status=400)
        
        if longitude is not None:
            if not (-180 <= longitude <= 180):
                return JsonResponse({'error': 'Longitude must be between -180 and 180'}, status=400)
        
        # Send to Firebase Cloud Messaging
        fcm_status = "not_sent"
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                topic=topic,
            )
            
            response = messaging.send(message)
            fcm_status = "sent"
        except Exception as e:
            print(f"Error sending to Firebase: {e}")
            response = "firebase-not-available"
            fcm_status = "error"
        
        # Save notification to database
        notification = Notification(
            title=title, 
            body=body, 
            topic=topic,
            emergency_type=alert_type,
            latitude=latitude,
            longitude=longitude,
            magnitude=magnitude,
            active=active,
            source=api_key_obj.entidad,
            api_key=api_key_obj
        )
        notification.save()
        
        # Guardar en Firestore según el tipo de alerta
        firestore_saved = False
        if alert_type == 'incendio':
            firestore_saved = save_fire_alert(
                title=title,
                body=body,
                latitude=latitude if latitude else -33.037542,
                longitude=longitude if longitude else -71.485482,
                active=active
            )
        elif alert_type == 'earthquake':
            firestore_saved = save_earthquake_alert(
                title=title,
                body=body,
                magnitude=magnitude if magnitude else 7.5,
                latitude=latitude if latitude else -33.050708,
                longitude=longitude if longitude else -71.435072,
                active=active
            )
        
        # Send to WebSocket clients
        NotificationConsumer.send_notification_to_group(
            'notifications',
            {
                'type': 'notification',
                'title': title,
                'body': body,
                'topic': topic,
                'source': api_key_obj.entidad
            }
        )
        
        return JsonResponse({
            'success': True, 
            'message_id': response,
            'fcm_status': fcm_status,
            'firestore_saved': firestore_saved,
            'alert_type': alert_type,
            'source': api_key_obj.entidad
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def list_alerts(request):
    """
    Lista todas las alertas (requiere API key válida)
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    try:
        api_key_obj = ApiKey.objects.get(key=api_key, is_active=True)
    except (ApiKey.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        alerts = Notification.objects.all().order_by('-created_at')[:50]
        data = [{
            'id': alert.id,
            'title': alert.title,
            'body': alert.body,
            'topic': alert.topic,
            'source': alert.source,
            'created_at': alert.created_at.isoformat()
        } for alert in alerts]
        
        return JsonResponse({'alerts': data, 'count': len(data)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_alert(request, alert_id):
    """
    Obtiene una alerta específica por ID
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    try:
        api_key_obj = ApiKey.objects.get(key=api_key, is_active=True)
    except (ApiKey.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        alert = Notification.objects.get(id=alert_id)
        data = {
            'id': alert.id,
            'title': alert.title,
            'body': alert.body,
            'topic': alert.topic,
            'source': alert.source,
            'created_at': alert.created_at.isoformat()
        }
        return JsonResponse(data)
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Alert not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def update_alert(request, alert_id):
    """
    Actualiza una alerta existente (requiere permisos de admin)
    """
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key and admin permissions
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    api_key_obj, error_response = check_admin_permission(api_key)
    if error_response:
        return error_response
    
    try:
        alert = Notification.objects.get(id=alert_id)
        data = json.loads(request.body)
        
        # Actualizar campos permitidos
        if 'title' in data:
            alert.title = data['title']
        if 'body' in data:
            alert.body = data['body']
        if 'topic' in data:
            alert.topic = data['topic']
        
        alert.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Alert updated successfully',
            'alert_id': alert.id,
            'updated_by': api_key_obj.entidad
        })
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Alert not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def delete_alert(request, alert_id):
    """
    Elimina una alerta (requiere permisos de admin)
    """
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key and admin permissions
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    api_key_obj, error_response = check_admin_permission(api_key)
    if error_response:
        return error_response
    
    try:
        alert = Notification.objects.get(id=alert_id)
        alert_title = alert.title
        alert.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Alert "{alert_title}" deleted successfully',
            'deleted_by': api_key_obj.entidad
        })
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Alert not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def validate_auth(request):
    """
    Valida una API key
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    try:
        api_key_obj = ApiKey.objects.get(key=api_key, is_active=True)
        return JsonResponse({
            'valid': True,
            'api_key_name': api_key_obj.name,
            'api_key_id': str(api_key_obj.key),
            'is_admin': api_key_obj.is_admin,
            'permissions': {
                'can_create_alerts': True,
                'can_view_alerts': True,
                'can_update_alerts': api_key_obj.is_admin,
                'can_delete_alerts': api_key_obj.is_admin,
                'can_manage_api_keys': api_key_obj.is_admin
            },
            'created_at': api_key_obj.created_at.isoformat(),
            'is_active': api_key_obj.is_active
        })
    except (ApiKey.DoesNotExist, ValueError):
        return JsonResponse({'valid': False, 'error': 'Invalid API key'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def list_api_keys(request):
    """
    Lista todas las API keys (requiere permisos de admin)
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key and admin permissions
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    api_key_obj, error_response = check_admin_permission(api_key)
    if error_response:
        return error_response
    
    try:
        api_keys = ApiKey.objects.all().order_by('-created_at')
        data = [{
            'id': key.id,
            'name': key.name,
            'key': str(key.key),
            'description': key.description,
            'is_admin': key.is_admin,
            'is_active': key.is_active,
            'created_at': key.created_at.isoformat()
        } for key in api_keys]
        
        return JsonResponse({'api_keys': data, 'count': len(data)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def create_api_key(request):
    """
    Crea una nueva API key (requiere permisos de admin)
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key and admin permissions
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    api_key_obj, error_response = check_admin_permission(api_key)
    if error_response:
        return error_response
    
    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        entidad = data.get('entidad', name)
        is_admin = data.get('is_admin', False)
        
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        
        # Crear nueva API key
        new_api_key = ApiKey.objects.create(
            name=name,
            entidad=entidad,
            description=description,
            is_admin=is_admin
        )
        
        return JsonResponse({
            'success': True,
            'message': 'API key created successfully',
            'api_key': {
                'id': new_api_key.id,
                'name': new_api_key.name,
                'key': str(new_api_key.key),
                'description': new_api_key.description,
                'is_admin': new_api_key.is_admin,
                'is_active': new_api_key.is_active,
                'created_at': new_api_key.created_at.isoformat()
            },
            'created_by': api_key_obj.entidad
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def revoke_api_key(request, key_id):
    """
    Revoca (desactiva) una API key (requiere permisos de admin)
    """
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Check API key and admin permissions
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return JsonResponse({'error': 'API key is required'}, status=401)
    
    api_key_obj, error_response = check_admin_permission(api_key)
    if error_response:
        return error_response
    
    try:
        target_key = ApiKey.objects.get(id=key_id)
        
        # No permitir que se revoque a sí mismo
        if str(target_key.key) == api_key:
            return JsonResponse({'error': 'Cannot revoke your own API key'}, status=400)
        
        target_key.is_active = False
        target_key.save()
        
        return JsonResponse({
            'success': True,
            'message': f'API key "{target_key.name}" revoked successfully',
            'revoked_key': {
                'id': target_key.id,
                'name': target_key.name,
                'key': str(target_key.key),
                'is_active': target_key.is_active
            },
            'revoked_by': api_key_obj.entidad
        })
    except ApiKey.DoesNotExist:
        return JsonResponse({'error': 'API key not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)