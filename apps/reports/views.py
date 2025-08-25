from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Report, ReportTemplate, DataExport, DashboardWidget
from .serializers import (
    ReportSerializer, ReportTemplateSerializer,
    DataExportSerializer, DashboardWidgetSerializer
)
from apps.users.permissions import IsConsultantOrAdmin
from apps.ticket.models import Ticket
from apps.landing.models import SelfAssessment, AssessmentResult

class ReportTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar plantillas de reportes.
    """
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsultantOrAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ReportTemplate.objects.none()
        return super().get_queryset()

class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar reportes.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsultantOrAdmin]

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Report.objects.none()
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def generate_ticket_summary(self, request):
        """
        Genera un reporte resumen de tickets
        """
        # Obtener estadísticas de tickets
        total_tickets = Ticket.objects.count()
        open_tickets = Ticket.objects.filter(status='open').count()
        closed_tickets = Ticket.objects.filter(status='closed').count()
        
        # Crear el reporte
        report_data = {
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'closed_tickets': closed_tickets,
            'generated_date': timezone.now().isoformat()
        }
        
        return Response(report_data)

class DataExportViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar exportaciones de datos.
    """
    queryset = DataExport.objects.all()
    serializer_class = DataExportSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsultantOrAdmin]

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return DataExport.objects.none()
        return super().get_queryset()

    @action(detail=False, methods=['post'])
    def export_tickets(self, request):
        """
        Exporta datos de tickets según filtros
        """
        filters = request.data.get('filters', {})
        export = DataExport.objects.create(
            name=f"Tickets Export {timezone.now()}",
            export_type='tickets',
            generated_by=request.user,
            filters=filters,
            status='processing'
        )
        # Aquí iría la lógica de exportación asíncrona
        return Response({'id': export.id, 'status': 'processing'})

class DashboardWidgetViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar widgets del dashboard.
    """
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsultantOrAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return DashboardWidget.objects.none()
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def get_metrics(self, request):
        """
        Obtiene métricas generales para el dashboard
        """
        # Métricas de tickets
        total_tickets = Ticket.objects.count()
        open_tickets = Ticket.objects.filter(status='open').count()
        
        # Métricas de autoevaluaciones
        total_assessments = SelfAssessment.objects.count()
        completed_assessments = AssessmentResult.objects.values('assessment').distinct().count()
        
        # Datos de los últimos 7 días
        last_week = timezone.now() - timedelta(days=7)
        new_tickets = Ticket.objects.filter(created_at__gte=last_week).count()
        
        metrics = {
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'total_assessments': total_assessments,
            'completed_assessments': completed_assessments,
            'new_tickets_last_week': new_tickets
        }
        
        return Response(metrics)
