from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_notification, name='send_notification'),
    path('broadcast/', views.broadcast_notification, name='broadcast_notification'),
    path('firebase/', views.send_firebase_notification, name='send_firebase_notification'),
    path('websocket/', views.send_websocket_notification, name='send_websocket_notification'),
]