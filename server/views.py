from django.shortcuts import render, redirect
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth, credentials, firestore, messaging
import json
import geopy.distance
import time
from firebase_config import db
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
def get_nearby_users(alerta_id):
    users = []
    # distancia evacuacion
    for punto_evacuacion in db.collection('alertas').document(alerta_id).get().to_dict()['puntos_evacuacion']:
        for user in db.collection('usuarios').stream():
            user_data = user.to_dict()
            user_coords = (user_data['location']['latitude'], user_data['location']['longitude'])
            if get_distance_coords(user_coords, (punto_evacuacion['latitude'], punto_evacuacion['longitude'])) <= db.collection('alertas').document(alerta_id).get().to_dict()['radios_evacuacion'][0]:
                users.append(user_data['fcmToken'])
    return users

def create_alert(request):
    title = "79 km E of Copiapó, Chile"
    puntos_evacuacion = [
        {'latitude': -27.3667, 'longitude': -70.3333},
        {'latitude': -27.3977, 'longitude': -70.3143},
        # Agrega más puntos de evacuación según sea necesario
    ]
    # time = ahora, obtener hora actual
    ts = time.time()
    type = 'incendio'
    # Crear una nueva alerta
    alerta_ref = db.collection('alertas').add({
        'title': title,
        'puntos_evacuacion': puntos_evacuacion,
        'radios_evacuacion': [12130982318092138,0.5],
        'type': type,
        'timestamp': ts,
        'activo': True
    })
    alerta_id = alerta_ref[1].id
    cherrypick(alerta_id)
    return render(request, 'dashboard.html')

def nuevosdatos(request):
    # imprime los datos de todas las alertas en json
    alertas = []
    alertas_ref = db.collection('alertas')
    for alerta in alertas_ref.stream():
        alertas.append(alerta.to_dict())
    return JsonResponse(alertas, safe=False)  # Establece safe=False para permitir listas

def cherrypick(alerta_id):
    # enviar notificacion a todos los usuarios cercanos
    users = get_nearby_users(alerta_id)
    registration_tokens = limpiarlista(users)
    
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title='Alerta de evacuación',
            body='¡Evacúa ahora!',
        ),
        data={'type': db.collection('alertas').document(alerta_id).get().to_dict()['type']},
        tokens=registration_tokens,
    )
    # Envía el mensaje multicast
    response = messaging.send_multicast(message)
    if response.failure_count > 0:
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(registration_tokens[idx])
        print('List of tokens that caused failures: {0}'.format(failed_tokens))

# si un elemento de la lista se repite eliminalo
def limpiarlista(lista):
    return list(dict.fromkeys(lista))