from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.ticket.models import Ticket, Message
from apps.landing.models import AssessmentResult
from .models import Notification

@receiver(post_save, sender=Ticket)
def create_ticket_notification(sender, instance, created, **kwargs):
    """Crear notificaciones cuando se crea o actualiza un ticket."""
    if created:
        # Notificar al consultor asignado si existe
        if instance.consultant:
            Notification.objects.create(
                user=instance.consultant,
                notification_type='ticket_created',
                title=f'Nuevo ticket asignado: {instance.subject}',
                message=f'Se te ha asignado un nuevo ticket de {instance.client.username}',
                content_object=instance
            )
    else:
        # Notificar cambios en el ticket
        if instance.status == 'closed':
            # Notificar al cliente
            Notification.objects.create(
                user=instance.client,
                notification_type='ticket_closed',
                title=f'Ticket cerrado: {instance.subject}',
                message='Tu ticket ha sido cerrado',
                content_object=instance
            )
        else:
            # Notificar actualización al cliente
            Notification.objects.create(
                user=instance.client,
                notification_type='ticket_updated',
                title=f'Ticket actualizado: {instance.subject}',
                message='Tu ticket ha sido actualizado',
                content_object=instance
            )

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """Crear notificaciones cuando se crea un nuevo mensaje."""
    if created:
        # Notificar al otro participante del ticket
        recipient = instance.ticket.client if instance.sender == instance.ticket.consultant else instance.ticket.consultant
        if recipient:
            Notification.objects.create(
                user=recipient,
                notification_type='message_created',
                title=f'Nuevo mensaje en ticket: {instance.ticket.subject}',
                message=f'Nuevo mensaje de {instance.sender.username}',
                content_object=instance
            )

@receiver(post_save, sender=AssessmentResult)
def create_assessment_notification(sender, instance, created, **kwargs):
    """Crear notificaciones cuando se completa una autoevaluación."""
    if created:
        # Notificar a los consultores
        from django.contrib.auth import get_user_model
        CustomUser = get_user_model()
        consultants = CustomUser.objects.filter(user_type='consultant')
        
        for consultant in consultants:
            Notification.objects.create(
                user=consultant,
                notification_type='assessment_completed',
                title=f'Nueva autoevaluación completada',
                message=f'El usuario {instance.user.username} ha completado una autoevaluación',
                content_object=instance
            )
