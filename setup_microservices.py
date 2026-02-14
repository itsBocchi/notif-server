#!/usr/bin/env python
"""
Script para configurar los microservicios del sistema de alertas
"""
import os
import sys
import django
import subprocess

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notif_server.settings')
django.setup()

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n[INFO] {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[SUCCESS] {description} completado exitosamente")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"[ERROR] Error en {description}")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[ERROR] Excepcion en {description}: {e}")
        return False
    return True

def setup_microservices():
    """Configura todos los microservicios"""
    print("Configurando Sistema de Alertas - Arquitectura de Microservicios")
    print("=" * 70)
    
    # Crear migraciones para cada servicio
    services = [
        ('auth_service', 'Authentication Service'),
        ('server', 'Alert Management Service (Core)'),
    ]
    
    for service, description in services:
        if not run_command(f'python manage.py makemigrations {service}', 
                          f'Creando migraciones para {description}'):
            return False
    
    # Aplicar todas las migraciones
    if not run_command('python manage.py migrate', 
                      'Aplicando todas las migraciones'):
        return False
    
    # Crear superusuario de Django (opcional)
    print("\n[INFO] Saltando creacion de superusuario (puedes crearlo manualmente despues)")
    print("   Para crear superusuario: python manage.py createsuperuser")
    
    # Crear API key de administrador
    print("\n[INFO] Creando API key de administrador...")
    try:
        from auth_service.models import ApiKey
        
        # Verificar si ya existe un admin
        existing_admin = ApiKey.objects.filter(is_admin=True).first()
        if existing_admin:
            print(f"[SUCCESS] Ya existe una API key de administrador: {existing_admin.name}")
            print(f"   Key: {existing_admin.key}")
        else:
            admin_key = ApiKey.objects.create(
                name="Sistema Administrador",
                description="API key principal para administradores del sistema",
                is_admin=True
            )
            print(f"[SUCCESS] API key de administrador creada exitosamente!")
            print(f"   Nombre: {admin_key.name}")
            print(f"   Key: {admin_key.key}")
            print(f"   [WARNING] IMPORTANTE: Guarda esta API key en un lugar seguro")
    except Exception as e:
        print(f"[ERROR] Error creando API key de administrador: {e}")
        return False
    
    print("\n[SUCCESS] Configuracion de microservicios completada exitosamente!")
    print("\n[INFO] Servicios disponibles:")
    print("   - Alert Management Service: /api/")
    print("   - Authentication Service: /auth/")
    print("   - Geospatial Service: /geo/")
    print("   - Notification Service: /notifications/")
    
    print("\n[INFO] Para iniciar el servidor:")
    print("   python manage.py runserver")
    
    print("\n[INFO] Para ejecutar las pruebas:")
    print("   python run_tests.py")
    
    return True

if __name__ == "__main__":
    success = setup_microservices()
    sys.exit(0 if success else 1)