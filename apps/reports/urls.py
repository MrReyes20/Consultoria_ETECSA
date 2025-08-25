from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'templates', views.ReportTemplateViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'exports', views.DataExportViewSet)
router.register(r'widgets', views.DashboardWidgetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
