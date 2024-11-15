from django.shortcuts import render, redirect
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth
import json
import geopy.distance

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

def get_distance_coords(coords1, coords2):
    return geopy.distance.distance(coords1, coords2).km

# Recuperar fcm de de cada usuario cuya locacion esta a menos de 1km del la coordenada 0,0 de la 
# coleccion usuarios
def get_nearby_users(document_id):
    users = []
    for user in firebase_config.db.collection('usuarios').stream():
        user_data = user.to_dict()
        user_coords = (user_data['latitude'], user_data['longitude'])
        # Obtener la alerta con el document_id
        alert = firebase_config.db.collection('alertas').document(document_id).get()
        if alert.exists:
            alert_data = alert.to_dict()
            evacuation_points = alert_data.get('puntos_evacuacion', [])
            evacuation_radii = alert_data.get('radios_evacuacion', [])

            # Calcular la distancia entre las coordenadas del usuario y los puntos de evacuación
            for point, radius in zip(evacuation_points, evacuation_radii):
                point_coords = (point['latitude'], point['longitude'])
                distance = get_distance_coords(user_coords, point_coords)
                if distance <= radius:
                    users.append(user_data['fcmToken'])
                    break
    return users