from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification

def index(request):
    """
    Render the main dashboard page
    """
    return render(request, 'index.html')

def dashboard(request):
    """
    Render the notification dashboard
    """
    notifications = Notification.objects.all().order_by('-created_at')[:50]
    return render(request, 'dashboard.html', {'notifications': notifications})

def get_notifications(request):
    """
    Return recent notifications as JSON
    """
    notifications = Notification.objects.all().order_by('-created_at')[:20]
    data = [{
        'id': n.id,
        'title': n.title,
        'body': n.body,
        'topic': n.topic,
        'source': n.source,
        'created_at': n.created_at.isoformat()
    } for n in notifications]
    
    return JsonResponse({'notifications': data})