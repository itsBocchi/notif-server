from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('authenticate/', views.authenticate_user, name='authenticate_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
]