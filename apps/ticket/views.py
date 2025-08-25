from rest_framework import generics, viewsets, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from rest_framework.throttling import UserRateThrottle
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from apps.ticket.models import Ticket, Message, TicketCategory, TicketAttachment
from apps.ticket.serializers import (
    TicketSerializer, MessageSerializer, TicketCategorySerializer,
    TicketAttachmentSerializer
)
from apps.users.permissions import IsConsultantOrAdmin, IsOwnerOrConsultant, IsAdminOnly

CustomUser = get_user_model()

class TicketRateThrottle(UserRateThrottle):
    rate = '10/minute'  # Limitar a 10 peticiones por minuto


class TicketCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar las categorías de tickets."""
    queryset = TicketCategory.objects.all()
    serializer_class = TicketCategorySerializer
    permission_classes = [IsConsultantOrAdmin]

class TicketListCreateView(generics.ListCreateAPIView):
    """
    API para listar y crear tickets.
    Los clientes solo ven sus propios tickets.
    Los consultores ven los tickets que les han sido asignados.
    Los administradores ven todos los tickets.
    """
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [TicketRateThrottle]
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['subject', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority', 'due_date']
    ordering = ['-created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # Solución para Swagger
            return Ticket.objects.none()

        user = self.request.user
        queryset = Ticket.objects.all()
        
        if not user.is_authenticated:
            return Ticket.objects.none()
            
        if hasattr(user, 'user_type'):
            if user.user_type == 'admin':
                pass  # Admin ve todos los tickets
            elif user.user_type == 'consultant':
                queryset = queryset.filter(consultant=user)
            else:  # cliente
                queryset = queryset.filter(client=user)
        else:
            return Ticket.objects.none()
            
        # Filtros adicionales
        status = self.request.query_params.get('status', None)
        priority = self.request.query_params.get('priority', None)
        category = self.request.query_params.get('category', None)
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'client':
            raise permissions.PermissionDenied("Solo los clientes pueden crear tickets.")

        # Crear el ticket y manejar archivos adjuntos
        ticket = serializer.save(client=user)


class TicketDetailView(generics.RetrieveUpdateAPIView):
    """
    API para ver y actualizar un ticket.
    Permisos basados en el rol del usuario.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrConsultant]
    parser_classes = (MultiPartParser, FormParser)

    def perform_update(self, serializer):
        ticket = serializer.instance
        old_status = ticket.status
        updated_ticket = serializer.save()
        
        # Si el ticket se cierra, registrar la fecha
        if old_status != 'closed' and updated_ticket.status == 'closed':
            updated_ticket.closed_at = timezone.now()
            updated_ticket.save()

class TicketAttachmentView(generics.CreateAPIView):
    """Vista para agregar archivos adjuntos a un ticket."""
    serializer_class = TicketAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrConsultant]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Verificar permisos
        if not IsOwnerOrConsultant().has_object_permission(self.request, self, ticket):
            raise permissions.PermissionDenied
        
        serializer.save(
            ticket=ticket,
            uploaded_by=self.request.user
        )
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        is_client = obj.client == user
        is_consultant = obj.consultant == user
        is_admin = user.user_type == 'admin'

        if not (is_client or is_consultant or is_admin):
            self.permission_denied(self.request, message="No tiene permisos para ver este ticket.")

        return obj

    def patch(self, request, *args, **kwargs):
        # Permisos para actualizar
        ticket = self.get_object()
        user = request.user
        if user.user_type not in ['admin', 'consultant']:
            return Response({"detail": "Solo los administradores y consultores pueden actualizar tickets."},
                            status=status.HTTP_403_FORBIDDEN)

        data = request.data
        if 'consultant' in data and user.user_type != 'admin':
            return Response({"detail": "Solo los administradores pueden asignar consultores."},
                            status=status.HTTP_403_FORBIDDEN)

        return self.partial_update(request, *args, **kwargs)


class MessageListView(APIView):
    """
    API para listar y crear mensajes dentro de un ticket.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ticket_pk = self.kwargs['ticket_pk']
        try:
            ticket = Ticket.objects.get(pk=ticket_pk)
            # Verificar permisos para ver los mensajes
            user = self.request.user
            if user.user_type == 'admin' or ticket.client == user or ticket.consultant == user:
                return Message.objects.filter(ticket=ticket).order_by('timestamp')
        except Ticket.DoesNotExist:
            return Message.objects.none()

        return Message.objects.none()

    def perform_create(self, serializer):
        ticket_pk = self.kwargs['ticket_pk']
        try:
            ticket = Ticket.objects.get(pk=ticket_pk)
            # Verificar si el usuario tiene permiso para responder
            user = self.request.user
            if user.user_type == 'admin' or ticket.client == user or ticket.consultant == user:
                serializer.save(ticket=ticket, sender=user)
            else:
                self.permission_denied(self.request, message="No tiene permisos para responder a este ticket.")
        except Ticket.DoesNotExist:
            self.permission_denied(self.request, message="Ticket no encontrado.")


class MessageCreateView:
    pass