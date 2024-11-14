from django.shortcuts import render, redirect
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth
import json

# Asegúrate de importar la configuración de Firebase
import firebase_config
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def authenticate_user(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            id_token = body.get('idToken')
            if not id_token:
                return JsonResponse({'status': 'error', 'message': 'ID token is missing'})
            
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            # Aquí puedes manejar la autenticación del usuario
            return JsonResponse({'status': 'success', 'uid': uid, 'redirect_url': '/dashboard/'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def home(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

from django.conf import settings

def firebase_config(request):
    config = {
        "apiKey": settings.FIREBASE_API_KEY,
        "authDomain": settings.FIREBASE_AUTH_DOMAIN,
        "projectId": settings.FIREBASE_PROJECT_ID,
        "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
        "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
        "appId": settings.FIREBASE_APP_ID,
    }
    return JsonResponse(config)