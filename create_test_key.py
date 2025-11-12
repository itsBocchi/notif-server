#!/usr/bin/env python
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notif_server.settings')

import django
django.setup()

from auth_service.models import ApiKey

# Crear API key para pruebas
api_key = ApiKey.objects.create(
    name="Testing Key",
    entidad="Test Organization",
    description="API key for testing purposes",
    is_active=True,
    is_admin=False
)

print("=" * 50)
print("API KEY PARA PRUEBAS CREADA")
print("=" * 50)
print(f"Nombre: {api_key.name}")
print(f"Entidad: {api_key.entidad}")
print(f"UUID: {api_key.key}")
print(f"Activa: {api_key.is_active}")
print("=" * 50)
print("Copia este UUID para usar en las pruebas:")
print(f"{api_key.key}")
print("=" * 50)