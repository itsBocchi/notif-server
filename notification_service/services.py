import firebase_admin
from firebase_admin import messaging
from server.consumers import NotificationConsumer
from utils.circuit_breaker import firebase_breaker, websocket_breaker, CircuitBreakerOpenException
import logging

logger = logging.getLogger(__name__)


class NotificationDeliveryService:
    """
    Servicio especializado en entrega de notificaciones
    Microservicio: Notification Delivery Service
    """
    
    @staticmethod
    def send_firebase_notification(title: str, body: str, topic: str = 'general', 
                                 data: dict = None) -> dict:
        """
        Envía notificación vía Firebase Cloud Messaging
        
        Args:
            title: Título de la notificación
            body: Cuerpo del mensaje
            topic: Tema de suscripción
            data: Datos adicionales
            
        Returns:
            Dict con resultado del envío
        """
        try:
            message_data = data or {}
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                topic=topic,
                data=message_data
            )
            
            response = messaging.send(message)
            logger.info(f"Firebase notification sent successfully: {response}")
            
            return {
                'success': True,
                'message_id': response,
                'channel': 'firebase_fcm',
                'topic': topic
            }
            
        except Exception as e:
            logger.error(f"Error sending Firebase notification: {e}")
            return {
                'success': False,
                'error': str(e),
                'channel': 'firebase_fcm'
            }
    
    @staticmethod
    def send_websocket_notification(group_name: str, message: dict) -> dict:
        """
        Envía notificación vía WebSocket
        
        Args:
            group_name: Nombre del grupo WebSocket
            message: Mensaje a enviar
            
        Returns:
            Dict con resultado del envío
        """
        try:
            NotificationConsumer.send_notification_to_group(group_name, {
                'type': 'notification',
                **message
            })
            
            logger.info(f"WebSocket notification sent to group: {group_name}")
            
            return {
                'success': True,
                'channel': 'websocket',
                'group': group_name
            }
            
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}")
            return {
                'success': False,
                'error': str(e),
                'channel': 'websocket'
            }
    
    @staticmethod
    def send_webhook_notification(webhook_urls: list, payload: dict) -> dict:
        """
        Envía notificaciones vía webhooks
        
        Args:
            webhook_urls: Lista de URLs de webhook
            payload: Datos a enviar
            
        Returns:
            Dict con resultado del envío
        """
        import requests
        
        results = []
        
        for url in webhook_urls:
            try:
                response = requests.post(
                    url, 
                    json=payload, 
                    timeout=5,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    results.append({
                        'url': url,
                        'success': True,
                        'status_code': response.status_code
                    })
                    logger.info(f"Webhook sent successfully to {url}")
                else:
                    results.append({
                        'url': url,
                        'success': False,
                        'status_code': response.status_code,
                        'error': f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                results.append({
                    'url': url,
                    'success': False,
                    'error': str(e)
                })
                logger.error(f"Error sending webhook to {url}: {e}")
        
        successful_sends = sum(1 for r in results if r['success'])
        
        return {
            'success': successful_sends > 0,
            'channel': 'webhook',
            'total_webhooks': len(webhook_urls),
            'successful_sends': successful_sends,
            'results': results
        }
    
    @staticmethod
    def send_multi_channel_notification(title: str, body: str, channels: dict) -> dict:
        """
        Envía notificación por múltiples canales
        
        Args:
            title: Título de la notificación
            body: Cuerpo del mensaje
            channels: Configuración de canales
            
        Returns:
            Dict con resultados de todos los canales
        """
        results = {}
        
        # Firebase Cloud Messaging
        if channels.get('firebase', {}).get('enabled', False):
            fcm_config = channels['firebase']
            results['firebase'] = NotificationDeliveryService.send_firebase_notification(
                title=title,
                body=body,
                topic=fcm_config.get('topic', 'general'),
                data=fcm_config.get('data', {})
            )
        
        # WebSocket
        if channels.get('websocket', {}).get('enabled', False):
            ws_config = channels['websocket']
            results['websocket'] = NotificationDeliveryService.send_websocket_notification(
                group_name=ws_config.get('group', 'notifications'),
                message={
                    'title': title,
                    'body': body,
                    **ws_config.get('data', {})
                }
            )
        
        # Webhooks
        if channels.get('webhooks', {}).get('enabled', False):
            webhook_config = channels['webhooks']
            results['webhooks'] = NotificationDeliveryService.send_webhook_notification(
                webhook_urls=webhook_config.get('urls', []),
                payload={
                    'title': title,
                    'body': body,
                    **webhook_config.get('data', {})
                }
            )
        
        # Calcular éxito general
        successful_channels = sum(1 for r in results.values() if r.get('success', False))
        
        return {
            'success': successful_channels > 0,
            'total_channels': len(results),
            'successful_channels': successful_channels,
            'results': results
        }