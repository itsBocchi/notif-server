import os
import firebase_admin
from firebase_admin import credentials, firestore

# Limpiar variables de entorno de Google Cloud
google_vars = ['GOOGLE_APPLICATION_CREDENTIALS', 'GOOGLE_CLOUD_PROJECT', 
               'GCLOUD_PROJECT', 'GOOGLE_CLOUD_QUOTA_PROJECT']
for var in google_vars:
    if var in os.environ:
        del os.environ[var]

# Configurar explícitamente
cred_path = 'serviceAccountKey.json'
project_id = 'alertduck-4746d'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(cred_path)
os.environ['GOOGLE_CLOUD_PROJECT'] = project_id

# Inicializar Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        default_app = firebase_admin.initialize_app(cred, {
            'projectId': project_id
        })
        print(f"✅ Firebase initialized: {project_id}")
    else:
        default_app = firebase_admin.get_app()
    
    # Crear cliente Firestore
    firestore_db = firestore.client(default_app)
    globals()['firestore_db'] = firestore_db
    
except Exception as e:
    print(f"❌ Firebase error: {e}")
    firestore_db = None