from rest_framework import serializers
from apps.ticket.models import Ticket, Message
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Message."""
    sender_username = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'ticket', 'sender', 'sender_username', 'content', 'timestamp']
        read_only_fields = ['ticket', 'sender']

class TicketSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Ticket, incluyendo mensajes anidados."""
    messages = MessageSerializer(many=True, read_only=True)
    client_username = serializers.ReadOnlyField(source='client.username')
    consultant_username = serializers.ReadOnlyField(source='consultant.username')

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'status', 'client', 'client_username', 'consultant', 'consultant_username', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['client', 'consultant'] # El cliente se asigna automáticamente, el consultor se asigna con PATCH

    def create(self, validated_data):
        # El cliente del ticket se asigna al usuario autenticado.
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)
