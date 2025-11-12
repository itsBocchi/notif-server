import requests
import json
import sys

def send_fire_alert(api_key, title, body, latitude=None, longitude=None, active=True):
    url = "http://localhost:8000/api/send-notification/"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    
    data = {
        "title": title,
        "body": body,
        "topic": "incendio",
        "type": "incendio",
        "active": active
    }
    
    if latitude is not None:
        data["latitude"] = latitude
    
    if longitude is not None:
        data["longitude"] = longitude
    
    print(f"Enviando alerta de incendio: {title}")
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python test_fire_alert.py <api_key> <título> [cuerpo] [latitud] [longitud] [activo]")
        sys.exit(1)
    
    api_key = sys.argv[1]
    title = sys.argv[2]
    body = sys.argv[3] if len(sys.argv) > 3 else "Alerta de incendio"
    latitude = float(sys.argv[4]) if len(sys.argv) > 4 else -33.037542
    longitude = float(sys.argv[5]) if len(sys.argv) > 5 else -71.485482
    active = sys.argv[6].lower() in ('true', 't', '1', 'yes', 'y') if len(sys.argv) > 6 else True
    
    send_fire_alert(api_key, title, body, latitude, longitude, active)