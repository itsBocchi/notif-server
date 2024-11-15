from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('authenticate/', views.authenticate_user, name='authenticate_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('firebase-config/', views.firebase_config, name='firebase_config'),
    path('datamore/', views.nuevosdatos, name='nuevosdatos'),
    path('create_alert/', views.create_alert, name='create_alert'),
]