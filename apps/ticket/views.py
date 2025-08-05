from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from apps.ticket.models import Ticket, Message
from apps.ticket.serializers import TicketSerializer, MessageSerializer

CustomUser = get_user_model()


class TicketListView(APIView):
    """
    API para listar y crear tickets.
    Los clientes solo ven sus propios tickets.
    Los consultores ven los tickets que les han sido asignados.
    Los administradores ven todos los tickets.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Ticket.objects.all().order_by('-created_at')
        elif user.user_type == 'consultant':
            return Ticket.objects.filter(consultant=user).order_by('-created_at')
        elif user.user_type == 'client':
            return Ticket.objects.filter(client=user).order_by('-created_at')
        return Ticket.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'client':
            # La restricción de creación se aplica en la vista
            return Response({"detail": "Solo los clientes pueden crear tickets."}, status=status.HTTP_403_FORBIDDEN)

        # El cliente del ticket se asigna al usuario autenticado.
        ticket = serializer.save(client=user)
        # Se asume que el primer mensaje se crea en una vista separada, o se puede crear aquí si se envía en el mismo payload.
        # Por simplicidad, se puede enviar el primer mensaje en el cuerpo de la solicitud y crearlo aquí.


class TicketDetailView(generics.RetrieveUpdateAPIView):
    """
    API para ver y actualizar un ticket.
    Permisos basados en el rol del usuario.
    """
    queryset = Ticket.objects.all()
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