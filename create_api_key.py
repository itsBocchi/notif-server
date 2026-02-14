import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notif_server.settings')
django.setup()

from auth_service.models import ApiKey

def create_api_key(name, description=None):
    api_key = ApiKey.objects.create(
        name=name,
        description=description or f"API key for {name}"
    )
    return api_key

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        name = input("Enter a name for the API key source: ")
    else:
        name = sys.argv[1]
    
    description = None
    if len(sys.argv) >= 3:
        description = sys.argv[2]
    
    api_key = create_api_key(name, description)
    print(f"\nAPI Key created successfully:")
    print(f"Name: {api_key.name}")
    print(f"Key: {api_key.key}")
    print(f"\nUse this key in the X-API-Key header when making requests to the API.")