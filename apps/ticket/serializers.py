from rest_framework import serializers
from apps.ticket.models import Ticket, Message, TicketCategory, TicketAttachment
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description']

class TicketAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.ReadOnlyField(source='uploaded_by.username')
    
    class Meta:
        model = TicketAttachment
        fields = ['id', 'file', 'file_name', 'file_type', 'file_size', 
                 'uploaded_by', 'uploaded_by_username', 'uploaded_at']
        read_only_fields = ['file_name', 'file_type', 'file_size', 'uploaded_by']

class MessageSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Message."""
    sender_username = serializers.ReadOnlyField(source='sender.username')
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Message
        fields = ['id', 'ticket', 'sender', 'sender_username', 'content', 
                 'timestamp', 'attachments', 'uploaded_files']
        read_only_fields = ['ticket', 'sender']

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        message = super().create(validated_data)
        
        for file in uploaded_files:
            TicketAttachment.objects.create(
                ticket=message.ticket,
                message=message,
                file=file,
                uploaded_by=message.sender
            )
        
        return message

class TicketSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Ticket, incluyendo mensajes y archivos adjuntos."""
    messages = MessageSerializer(many=True, read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    client_username = serializers.ReadOnlyField(source='client.username')
    consultant_username = serializers.ReadOnlyField(source='consultant.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'status', 'priority', 'category', 
                 'category_name', 'client', 'client_username', 'consultant', 
                 'consultant_username', 'resolution', 'due_date', 'created_at', 
                 'updated_at', 'closed_at', 'messages', 'attachments', 'uploaded_files']
        read_only_fields = ['client', 'consultant', 'closed_at']

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        validated_data['client'] = self.context['request'].user
        ticket = super().create(validated_data)
        
        for file in uploaded_files:
            TicketAttachment.objects.create(
                ticket=ticket,
                file=file,
                uploaded_by=ticket.client
            )
        
        return ticket

    def update(self, instance, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        ticket = super().update(instance, validated_data)
        
        for file in uploaded_files:
            TicketAttachment.objects.create(
                ticket=ticket,
                file=file,
                uploaded_by=self.context['request'].user
            )
        
        # Si el estado cambia a cerrado, registrar la fecha
        if validated_data.get('status') == 'closed' and instance.status != 'closed':
            from django.utils import timezone
            ticket.closed_at = timezone.now()
            ticket.save()
        
        return ticket
