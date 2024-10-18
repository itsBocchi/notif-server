import firebase_admin
from firebase_admin import credentials

# Reemplaza 'path/to/serviceAccountKey.json' con la ruta a tu archivo de clave de cuenta de servicio
cred = credentials.Certificate('alertduckaccountkey.json')
firebase_admin.initialize_app(cred)