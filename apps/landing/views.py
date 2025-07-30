
from rest_framework import generics, permissions
from rest_framework.response import Response

from . import serializers
from .models import Section, Service, SuccessCase, ContactMessage, SelfAssessment
from .serializers import (
    SectionSerializer,
    ServiceSerializer,
    SuccessCaseSerializer,
    ContactMessageSerializer,
    SelfAssessmentSerializer
)


class PublicContentView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sections = Section.objects.all()
        services = Service.objects.all()
        success_cases = SuccessCase.objects.all()

        return Response({
            'sections': SectionSerializer(sections, many=True).data,
            'services': ServiceSerializer(services, many=True).data,
            'success_cases': SuccessCaseSerializer(success_cases, many=True).data
        })


class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if "spam" in serializer.validated_data['message'].lower():
            raise serializers.ValidationError("El mensaje contiene contenido no permitido")
        serializer.save()


class SelfAssessmentListView(generics.ListAPIView):
    queryset = SelfAssessment.objects.all()
    serializer_class = SelfAssessmentSerializer
    permission_classes = [permissions.AllowAny]