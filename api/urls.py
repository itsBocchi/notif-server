from django.urls import path
from . import views

urlpatterns = [
    path('send-notification/', views.send_notification, name='send_notification'),
    path('alerts/', views.list_alerts, name='list_alerts'),
    path('alerts/<int:alert_id>/', views.get_alert, name='get_alert'),
    path('alerts/<int:alert_id>/update/', views.update_alert, name='update_alert'),
    path('alerts/<int:alert_id>/delete/', views.delete_alert, name='delete_alert'),
    path('auth/validate/', views.validate_auth, name='validate_auth'),
    path('api-keys/', views.list_api_keys, name='list_api_keys'),
    path('api-keys/create/', views.create_api_key, name='create_api_key'),
    path('api-keys/<int:key_id>/revoke/', views.revoke_api_key, name='revoke_api_key'),
]