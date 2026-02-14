import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from django.db import transaction

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "notifications"
        self.room_group_name = f"notifications_group"
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'notification':
            title = text_data_json.get('title')
            body = text_data_json.get('body')
            topic = text_data_json.get('topic', 'general')
            source = text_data_json.get('source')
            
            # Save to database
            await self.save_notification(title, body, topic, source)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'title': title,
                    'body': body,
                    'topic': topic,
                    'source': source
                }
            )
    
    # Receive message from room group
    async def notification_message(self, event):
        title = event['title']
        body = event['body']
        topic = event.get('topic', 'general')
        source = event.get('source')
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': title,
            'body': body,
            'topic': topic,
            'source': source
        }))
    
    @staticmethod
    def send_notification_to_group(group_name, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"{group_name}_group",
            message
        )
    
    @staticmethod
    async def save_notification(title, body, topic, source=None):
        # This needs to be run in a transaction since it's called from an async context
        @transaction.atomic
        def save():
            notification = Notification(title=title, body=body, topic=topic, source=source)
            notification.save()
            return notification
        
        # Run the save function in a sync_to_async context
        from asgiref.sync import sync_to_async
        await sync_to_async(save)()