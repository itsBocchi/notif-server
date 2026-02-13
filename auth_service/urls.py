from django.urls import path
from . import views

urlpatterns = [
    path('validate/', views.validate_api_key, name='validate_api_key'),
    path('api-keys/', views.list_api_keys, name='list_api_keys'),
    path('api-keys/create/', views.create_api_key, name='create_api_key'),
    path('api-keys/<int:key_id>/revoke/', views.revoke_api_key, name='revoke_api_key'),
]