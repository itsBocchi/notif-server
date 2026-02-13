#!/usr/bin/env python
"""
Script para crear una API key con permisos de administrador
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notif_server.settings')
django.setup()

from auth_service.models import ApiKey

def create_admin_api_key(name, description=""):
    """
    Crea una nueva API key con permisos de administrador
    """
    try:
        api_key = ApiKey.objects.create(
            name=name,
            description=description,
            is_admin=True
        )
        
        print(f"✅ API key de administrador creada exitosamente!")
        print(f"📋 Nombre: {api_key.name}")
        print(f"🔑 API Key: {api_key.key}")
        print(f"👑 Permisos: Administrador")
        print(f"📅 Creada: {api_key.created_at}")
        print("\n⚠️  IMPORTANTE: Guarda esta API key en un lugar seguro.")
        print("   No podrás verla nuevamente una vez que cierres esta ventana.")
        
        return str(api_key.key)
        
    except Exception as e:
        print(f"❌ Error al crear la API key: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python create_admin_api_key.py <nombre_organizacion> [descripcion]")
        print("Ejemplo: python create_admin_api_key.py \"ONEMI\" \"API key para administradores ONEMI\"")
        sys.exit(1)
    
    name = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else f"API key de administrador para {name}"
    
    create_admin_api_key(name, description)