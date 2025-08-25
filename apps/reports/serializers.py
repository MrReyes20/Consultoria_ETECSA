from rest_framework import serializers
from .models import Report, ReportTemplate, DataExport, DashboardWidget

class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ['id', 'name', 'description', 'template_type', 'created_at', 
                 'updated_at', 'created_by', 'template_data']
        read_only_fields = ['created_at', 'updated_at', 'created_by']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'template', 'name', 'description', 'generated_by', 
                 'generated_at', 'parameters', 'file', 'status', 'error_message',
                 'content_type', 'object_id']
        read_only_fields = ['generated_at', 'generated_by', 'status', 'error_message']

class DataExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataExport
        fields = ['id', 'name', 'description', 'export_type', 'generated_by',
                 'generated_at', 'file', 'filters', 'status', 'error_message']
        read_only_fields = ['generated_at', 'generated_by', 'status', 'error_message']

class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = ['id', 'name', 'description', 'widget_type', 'configuration',
                 'created_by', 'created_at', 'updated_at', 'is_active', 'position']
        read_only_fields = ['created_at', 'updated_at', 'created_by']
