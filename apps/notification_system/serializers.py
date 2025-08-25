from rest_framework import serializers
from .models import Notification, NotificationPreference

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Notification
    """
    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'title', 'message', 
                 'read', 'created_at', 'content_type', 'object_id']
        read_only_fields = ['created_at']

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo NotificationPreference
    """
    class Meta:
        model = NotificationPreference
        fields = ['id', 'user',
                 'email_ticket_created', 'email_ticket_updated', 'email_ticket_closed',
                 'email_message_created', 'email_assessment_completed',
                 'web_ticket_created', 'web_ticket_updated', 'web_ticket_closed',
                 'web_message_created', 'web_assessment_completed']
        read_only_fields = ['user']
