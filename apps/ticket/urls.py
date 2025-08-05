# from .views import TicketListView, TicketDetailView, MessageListView
# from apps.tickets.models import Ticket
#
# router = DefaultRouter()
# router.register(r'tickets', TicketListView, basename='tickets')
# router.register(r'tickets/(?P<ticket_pk>\d+)/messages', MessageListView, basename='ticket-messages')
# router.register(r'tickets/(?P<pk>\d+)', TicketDetailView, basename='ticket-detail')
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]


from django.urls import path
from apps.ticket.views import TicketListView, TicketDetailView, MessageListView, MessageCreateView

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:ticket_pk>/messages/', MessageListView.as_view(), name='message-list'),
    # path('<int:ticket_pk>/messages/create/', MessageCreateView.as_view(), name='message-create'),
]