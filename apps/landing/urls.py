# apps/landing/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicContentView,
    ContactCreateView,
    SelfAssessmentListView,
    SectionViewSet,
    ServiceViewSet,
    SuccessCaseViewSet,
    SelfAssessmentViewSet,
    AssessmentQuestionViewSet,
    UserResponseCreateView,
    AssessmentResultCreateView,
    UserAssessmentResultsView,
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
router.register(r'questions', AssessmentQuestionViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    # Rutas públicas existentes
    path('content/', PublicContentView.as_view(), name='public-content'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    path('assessments-public/', SelfAssessmentListView.as_view(), name='assessments-list-public'),

    # Rutas de la API administrable (usando routers)
    path('', include(router.urls)),

    # Rutas para la autoevaluación
    path('user-responses/', UserResponseCreateView.as_view(), name='user-response-create'),
    path('assessment-results/', AssessmentResultCreateView.as_view(), name='assessment-result-create'),
    path('my-assessment-results/', UserAssessmentResultsView.as_view(), name='user-assessment-results'),
]
