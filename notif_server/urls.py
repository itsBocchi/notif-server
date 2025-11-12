"""
URL configuration for notif_server project.
Microservices Architecture
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Alert Management Service (Core)
    path('api/', include('api.urls')),
    
    # Authentication Service
    path('auth/', include('auth_service.urls')),
    
    # Geospatial Processing Service
    path('geo/', include('geo.urls')),
    
    # Notification Delivery Service
    path('notifications/', include('notification_service.urls')),
    
    # Dashboard and static content
    path('', include('server.urls')),
]