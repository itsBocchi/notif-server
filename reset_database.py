import os
import django
import shutil

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notif_server.settings')
django.setup()

# Importar después de configurar Django
from django.db import connection
from django.conf import settings
import firebase_admin
from firebase_admin import firestore

def reset_sqlite_database():
    """Elimina y recrea la base de datos SQLite"""
    try:
        # Cerrar conexiones a la base de datos
        connection.close()
        
        # Ruta a la base de datos
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        
        # Eliminar archivo de base de datos si existe
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Base de datos SQLite eliminada: {db_path}")
        
        # Ejecutar migraciones para recrear la base de datos
        os.system('python manage.py migrate')
        print("Base de datos SQLite recreada con éxito")
        
        # Crear superusuario
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("Superusuario 'admin' creado con contraseña 'admin123'")
        
        return True
    except Exception as e:
        print(f"Error al reiniciar la base de datos SQLite: {e}")
        return False

def reset_firestore_collection():
    """Elimina todos los documentos de la colección 'alertas' en Firestore"""
    try:
        # Obtener instancia de Firestore
        db = None
        try:
            db = firestore.client()
        except ValueError:
            # Si no hay una app inicializada, inicializar con credenciales
            cred_path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
            if os.path.exists(cred_path):
                from firebase_admin import credentials
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                db = firestore.client()
        
        if not db:
            print("No se pudo conectar a Firestore")
            return False
        
        # Eliminar todos los documentos de la colección 'alertas'
        alertas_ref = db.collection('alertas')
        docs = alertas_ref.stream()
        
        count = 0
        for doc in docs:
            doc.reference.delete()
            count += 1
        
        print(f"Se eliminaron {count} documentos de la colección 'alertas' en Firestore")
        return True
    except Exception as e:
        print(f"Error al reiniciar la colección de Firestore: {e}")
        return False

if __name__ == "__main__":
    print("Reiniciando bases de datos...")
    
    # Reiniciar SQLite
    sqlite_reset = reset_sqlite_database()
    
    # Reiniciar Firestore
    firestore_reset = reset_firestore_collection()
    
    if sqlite_reset and firestore_reset:
        print("\n✅ Bases de datos reiniciadas con éxito")
    else:
        print("\n⚠️ Hubo problemas al reiniciar las bases de datos")
    
    # Crear una API key de ejemplo
    try:
        from server.models import ApiKey
        key = ApiKey.objects.create(name='Sistema de Alertas de Catástrofe', 
                                   description='API key para el sistema de alertas de catástrofe')
        print(f"\nAPI Key creada: {key.key}")
        print("Nombre: Sistema de Alertas de Catástrofe")
    except Exception as e:
        print(f"Error al crear API key: {e}")