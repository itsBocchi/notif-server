from django.urls import path
from . import views

urlpatterns = [
    path('validate-coordinates/', views.validate_coordinates, name='validate_coordinates'),
    path('calculate-evacuation-zone/', views.calculate_evacuation_zone, name='calculate_evacuation_zone'),
    path('calculate-evacuation-radius/', views.calculate_evacuation_radius, name='calculate_evacuation_radius'),
    path('find-evacuation-points/', views.find_evacuation_points, name='find_evacuation_points'),
]