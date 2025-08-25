from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

CustomUser = get_user_model()

class Notification(models.Model):
    """Modelo para notificaciones del sistema."""
    NOTIFICATION_TYPES = (
        ('ticket_created', 'Nuevo Ticket Creado'),
        ('ticket_updated', 'Ticket Actualizado'),
        ('ticket_closed', 'Ticket Cerrado'),
        ('message_created', 'Nuevo Mensaje'),
        ('assessment_completed', 'Autoevaluación Completada'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Campos para referencia genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.title}"

class NotificationPreference(models.Model):
    """Preferencias de notificación por usuario."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Notificaciones por email
    email_ticket_created = models.BooleanField(default=True)
    email_ticket_updated = models.BooleanField(default=True)
    email_ticket_closed = models.BooleanField(default=True)
    email_message_created = models.BooleanField(default=True)
    email_assessment_completed = models.BooleanField(default=True)
    
    # Notificaciones en plataforma
    web_ticket_created = models.BooleanField(default=True)
    web_ticket_updated = models.BooleanField(default=True)
    web_ticket_closed = models.BooleanField(default=True)
    web_message_created = models.BooleanField(default=True)
    web_assessment_completed = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferencias de notificación para {self.user.username}"
