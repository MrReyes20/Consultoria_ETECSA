# apps/landing/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    PublicContentView,
    ContactCreateView,
    SelfAssessmentListView,
    SectionViewSet,
    ServiceViewSet,
    SuccessCaseViewSet,
    SelfAssessmentViewSet,
    AssessmentQuestionViewSet,
    PostViewSet,
    CommentViewSet
)

# Router principal para las vistas de nivel superior
router = DefaultRouter()
router.register(r'sections', SectionViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'success-cases', SuccessCaseViewSet)
router.register(r'assessments', SelfAssessmentViewSet)
router.register(r'posts', PostViewSet)


assessments_router = routers.NestedSimpleRouter(router, r'assessments', lookup='assessment')
assessments_router.register(r'questions', AssessmentQuestionViewSet, basename='assessment-questions')

posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')


urlpatterns = [
    # Rutas públicas existentes
    path('content/', PublicContentView.as_view(), name='public-content'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    path('assessments-public/', SelfAssessmentListView.as_view(), name='assessments-list-public'), # Renombrado para evitar conflicto con el ViewSet

    # Rutas de la API administrable (usando routers)
    path('', include(router.urls)),
    path('', include(assessments_router.urls)), # Incluye las rutas anidadas de preguntas
    path('', include(posts_router.urls)), # Incluye las rutas anidadas de comentarios
]
