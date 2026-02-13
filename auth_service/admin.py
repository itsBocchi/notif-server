from django.contrib import admin
from .models import ApiKey

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'is_active', 'is_admin', 'created_at')
    list_filter = ('is_active', 'is_admin', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('key',)