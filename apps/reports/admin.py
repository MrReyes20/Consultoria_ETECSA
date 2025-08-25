from django.contrib import admin
from .models import Report, ReportTemplate, DataExport

admin.site.register(Report)
admin.site.register(ReportTemplate)
admin.site.register(DataExport)
