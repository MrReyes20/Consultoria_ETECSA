from django.urls import path, include
from apps.landing.views import PublicContentView, ContactCreateView, SelfAssessmentListView

urlpatterns = [
    path('api/landing/content/', PublicContentView.as_view(), name='public-content'),
    path('api/landing/contact/', ContactCreateView.as_view(), name='contact-create'),
    path('api/landing/assessments/', SelfAssessmentListView.as_view(), name='assessments-list'),
]