from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'source', 'created_at')
    list_filter = ('topic', 'source', 'created_at')
    search_fields = ('title', 'body')