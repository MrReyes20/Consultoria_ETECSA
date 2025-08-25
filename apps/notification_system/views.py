from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer
from apps.users.permissions import IsOwnerOrConsultant

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar notificaciones.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrConsultant]

    def get_queryset(self):
        """
        Filtra las notificaciones para mostrar solo las del usuario actual
        o todas si es un consultor.
        """
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
            
        user = self.request.user
        if user.is_consultant or user.is_staff:
            return Notification.objects.all()
        return Notification.objects.filter(user=user)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Marca todas las notificaciones del usuario como leídas
        """
        self.get_queryset().filter(user=request.user).update(read=True)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Marca una notificación específica como leída
        """
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response(status=status.HTTP_200_OK)

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar preferencias de notificación.
    """
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra las preferencias para mostrar solo las del usuario actual
        o todas si es un administrador.
        """
        if getattr(self, 'swagger_fake_view', False):
            return NotificationPreference.objects.none()
            
        user = self.request.user
        if user.is_staff:
            return NotificationPreference.objects.all()
        return NotificationPreference.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Al crear una nueva preferencia, asegura que esté asociada al usuario actual
        """
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Actualiza las preferencias de notificación del usuario
        """
        instance = self.get_object()
        # Verifica que el usuario solo pueda actualizar sus propias preferencias
        if instance.user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
