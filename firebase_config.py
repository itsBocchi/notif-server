import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
try:
    cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'serviceAccountKey.json')
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        default_app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        print(f"Firebase initialized successfully with credentials from {cred_path}")
        # Exportar la instancia de Firestore para uso en otras partes de la aplicación
        globals()['firestore_db'] = db
    else:
        # Initialize with a mock app for development
        default_app = firebase_admin.initialize_app()
        print("Firebase initialized with default app (MOCK MODE)")
        print("WARNING: FCM notifications will not be sent to mobile devices")
        print(f"To enable FCM, create a service account key file at {cred_path}")
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    # Initialize with a mock app for development
    if not firebase_admin._apps:
        default_app = firebase_admin.initialize_app()
        print("Firebase initialized with default app (MOCK MODE)")
    else:
        default_app = firebase_admin.get_app()