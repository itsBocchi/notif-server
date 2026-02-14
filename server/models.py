from django.db import models
import uuid

class Notification(models.Model):
    """
    Modelo para almacenar notificaciones de emergencia en la base de datos local.
    Microservicio: Alert Management Service (Core)
    """
    title = models.CharField(max_length=255, help_text="Título descriptivo del evento")
    body = models.TextField(help_text="Descripción detallada de la emergencia")
    topic = models.CharField(max_length=100, default='general', help_text="Categoría de la notificación")
    emergency_type = models.CharField(max_length=50, default='general', help_text="Tipo de emergencia")
    latitude = models.FloatField(null=True, blank=True, help_text="Latitud del evento")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitud del evento")
    magnitude = models.FloatField(null=True, blank=True, help_text="Magnitud (para terremotos)")
    active = models.BooleanField(default=True, help_text="Estado activo de la emergencia")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp del evento")
    source = models.CharField(max_length=150, null=True, blank=True, help_text="Organismo que generó la alerta")
    api_key = models.ForeignKey('auth_service.ApiKey', on_delete=models.SET_NULL, null=True, blank=True, help_text="API Key que creó la alerta")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notificación de Emergencia"
        verbose_name_plural = "Notificaciones de Emergencia"
    
    def save(self, *args, **kwargs):
        # Auto-llenar source desde api_key.entidad
        if self.api_key and not self.source:
            self.source = self.api_key.entidad
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.source or 'Sin fuente'}"

class ApiKey(models.Model):
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('admin', 'Administrador'),
    ]
    
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.role}) - {self.key}"