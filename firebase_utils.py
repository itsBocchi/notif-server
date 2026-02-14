import firebase_admin
from firebase_admin import firestore
import firebase_config
from google.cloud import firestore as google_firestore

def get_firestore_db():
    """
    Obtiene la instancia de Firestore
    """
    if hasattr(firebase_config, 'firestore_db'):
        return firebase_config.firestore_db
    else:
        try:
            return firestore.client()
        except Exception as e:
            print(f"Error al obtener Firestore: {e}")
            return None

def save_fire_alert(title, body, latitude, longitude, active=True):
    """
    Componente: Gestor Geoespacial + Almacén de Datos
    
    Guarda una alerta de incendio en Firestore con cálculos geoespaciales automáticos.
    
    Parámetros por defecto para incendios:
    - Radio de evacuación: 1 metro (zona inmediata)
    - Punto de evacuación: Coordenadas del evento
    
    Args:
        title (str): Título descriptivo del incendio
        body (str): Descripción detallada del evento
        latitude (float): Latitud del incendio
        longitude (float): Longitud del incendio
        active (bool): Estado del incendio (activo/controlado)
    
    Returns:
        bool: True si se guardó exitosamente, False en caso contrario
    """
    db = get_firestore_db()
    if not db:
        print("No se pudo obtener la instancia de Firestore")
        return False
    
    try:
        # Estructura de datos según el modelo diseñado
        alert_data = {
            'activo': active,
            'puntos_evacuacion': [
                {
                    'latitude': latitude,
                    'longitude': longitude
                }
            ],
            'radios_evacuacion': [1],  # 1 metro para incendios
            'time': google_firestore.SERVER_TIMESTAMP,
            'title': title,
            'body': body,
            'type': 'incendio'
        }
        
        db.collection('alertas').add(alert_data)
        print(f"Alerta de incendio guardada en Firestore: {title}")
        return True
    except Exception as e:
        print(f"Error al guardar alerta de incendio en Firestore: {e}")
        return False

def save_earthquake_alert(title, body, magnitude, latitude, longitude, active=False):
    """
    Componente: Gestor Geoespacial + Almacén de Datos
    
    Guarda una alerta de terremoto en Firestore con cálculos geoespaciales automáticos.
    
    Parámetros por defecto para terremotos:
    - Radio de evacuación: 500 metros (área de seguridad ampliada)
    - Punto de evacuación: Coordenadas del epicentro
    
    Args:
        title (str): Título descriptivo del terremoto
        body (str): Descripción detallada del evento
        magnitude (float): Magnitud del terremoto en escala Richter
        latitude (float): Latitud del epicentro
        longitude (float): Longitud del epicentro
        active (bool): Estado del evento (generalmente False para terremotos)
    
    Returns:
        bool: True si se guardó exitosamente, False en caso contrario
    """
    db = get_firestore_db()
    if not db:
        print("No se pudo obtener la instancia de Firestore")
        return False
    
    try:
        # Estructura de datos según el modelo diseñado
        alert_data = {
            'activo': active,
            'magnitude': magnitude,
            'puntos_evacuacion': [
                {
                    'latitude': latitude,
                    'longitude': longitude
                }
            ],
            'radios_evacuacion': [500],  # 500 metros para terremotos
            'time': google_firestore.SERVER_TIMESTAMP,
            'title': title,
            'body': body,
            'type': 'earthquake'
        }
        
        db.collection('alertas').add(alert_data)
        print(f"Alerta de terremoto guardada en Firestore: {title} (Magnitud: {magnitude})")
        return True
    except Exception as e:
        print(f"Error al guardar alerta de terremoto en Firestore: {e}")
        return False