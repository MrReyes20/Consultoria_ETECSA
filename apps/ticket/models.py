from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class TicketCategory(models.Model):
    """Modelo para las categorías de tickets."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ticket Categories"

class Ticket(models.Model):
    """Modelo para representar un ticket de soporte."""
    app_label = 'ticket'
    STATUS_CHOICES = [
        ('new', 'Nuevo'),
        ('open', 'Abierto'),
        ('in_progress', 'En Progreso'),
        ('pending', 'Pendiente'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]

    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.ForeignKey(TicketCategory, on_delete=models.SET_NULL, null=True, related_name='tickets')
    
    # Relaciones con el modelo de usuario
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_tickets')
    consultant = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='consultant_tickets')
    
    # Campos de seguimiento
    resolution = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

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

class TicketAttachment(models.Model):
    """Modelo para archivos adjuntos en tickets y mensajes."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    file = models.FileField(upload_to='ticket_attachments/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    file_size = models.IntegerField()  # Tamaño en bytes
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adjunto {self.file_name} en Ticket #{self.ticket.pk}"

    def save(self, *args, **kwargs):
        if not self.file_name:
            self.file_name = self.file.name
        if not self.file_size:
            self.file_size = self.file.size
        if not self.file_type:
            self.file_type = self.file.content_type
        super().save(*args, **kwargs)
