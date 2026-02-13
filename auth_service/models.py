from django.db import models
import uuid

class ApiKey(models.Model):
    """
    Modelo para gestionar claves de API del sistema de autenticación.
    Microservicio: Authentication Service
    """
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, help_text="Clave UUID única")
    name = models.CharField(max_length=100, help_text="Nombre identificatorio técnico")
    entidad = models.CharField(max_length=150, help_text="Nombre oficial del organismo autorizado")
    description = models.TextField(blank=True, null=True, help_text="Descripción del uso de la clave")
    is_active = models.BooleanField(default=True, help_text="Estado de la clave de acceso")
    is_admin = models.BooleanField(default=False, help_text="Permisos de administrador")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Clave de API"
        verbose_name_plural = "Claves de API"
        app_label = 'auth_service'
    
    def __str__(self):
        admin_text = " (Admin)" if self.is_admin else ""
        return f"{self.entidad}{admin_text} ({'Activa' if self.is_active else 'Inactiva'})"
    
    def is_valid(self):
        """Verifica si la API key es válida y activa"""
        return self.is_active