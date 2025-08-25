from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

CustomUser = get_user_model()

class ReportTemplate(models.Model):
    """Modelo para plantillas de reportes"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    template_type = models.CharField(max_length=50, choices=[
        ('pdf', 'PDF Report'),
        ('excel', 'Excel Report'),
        ('csv', 'CSV Export'),
        ('custom', 'Custom Report')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    template_data = models.JSONField(default=dict)  # Configuración específica del reporte

    def __str__(self):
        return self.name

class Report(models.Model):
    """Modelo para reportes generados"""
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    generated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    parameters = models.JSONField(default=dict)  # Parámetros usados para generar el reporte
    file = models.FileField(upload_to='reports/%Y/%m/%d/')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    error_message = models.TextField(blank=True)

    # Para referencias genéricas (por ejemplo, reportes específicos de tickets o usuarios)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.name} - {self.generated_at}"

class DataExport(models.Model):
    """Modelo para exportaciones de datos"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    export_type = models.CharField(max_length=50, choices=[
        ('tickets', 'Tickets Export'),
        ('users', 'Users Export'),
        ('assessments', 'Assessments Export'),
        ('notifications', 'Notifications Export'),
        ('custom', 'Custom Export')
    ])
    generated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='exports/%Y/%m/%d/')
    filters = models.JSONField(default=dict)  # Filtros aplicados en la exportación
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.generated_at}"

class DashboardWidget(models.Model):
    """Modelo para widgets del dashboard"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    widget_type = models.CharField(max_length=50, choices=[
        ('chart', 'Chart'),
        ('metric', 'Metric'),
        ('table', 'Table'),
        ('custom', 'Custom Widget')
    ])
    configuration = models.JSONField(default=dict)  # Configuración específica del widget
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(default=0)  # Para ordenar widgets en el dashboard

    def __str__(self):
        return self.name
