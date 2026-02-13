import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notif_server.settings')
django.setup()

# Importar después de configurar Django
import firebase_admin
from firebase_admin import firestore, credentials

def reset_firestore_collection():
    """Elimina todos los documentos de la colección 'alertas' en Firestore"""
    try:
        # Obtener instancia de Firestore
        db = None
        try:
            db = firestore.client()
        except ValueError:
            # Si no hay una app inicializada, inicializar con credenciales
            cred_path = 'serviceAccountKey.json'
            if os.path.exists(cred_path):
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
    print("Reiniciando colección 'alertas' en Firestore...")
    success = reset_firestore_collection()
    
    if success:
        print("✅ Colección reiniciada con éxito")
    else:
        print("❌ Error al reiniciar la colección")
        sys.exit(1)