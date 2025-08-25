from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.ticket.views import (
    TicketListCreateView,
    TicketDetailView,
    TicketCategoryViewSet,
    TicketAttachmentView,
    MessageListView,
    MessageCreateView
)

# Configurar el router para las vistas basadas en viewsets
router = DefaultRouter()
router.register(r'categories', TicketCategoryViewSet, basename='ticket-category')

urlpatterns = [
    # Incluir las URLs del router
    path('', include(router.urls)),
    
    # URLs para tickets
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:ticket_id>/attachments/', TicketAttachmentView.as_view(), name='ticket-attachment'),
    
    # URLs para mensajes
    path('tickets/<int:ticket_pk>/messages/', MessageListView.as_view(), name='message-list'),
]