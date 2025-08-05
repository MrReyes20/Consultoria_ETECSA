from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Ticket(models.Model):
    """Modelo para representar un ticket de soporte."""
    app_label = 'ticket'
    STATUS_CHOICES = [
        ('new', 'Nuevo'),
        ('open', 'Abierto'),
        ('in_progress', 'En Progreso'),
        ('closed', 'Cerrado'),
    ]

    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Relaciones con el modelo de usuario
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_tickets')
    consultant = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='consultant_tickets')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.pk}: {self.subject}"


class Message(models.Model):
    """Modelo para los mensajes dentro de un ticket."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.sender.username} en Ticket #{self.ticket.pk}"
