# landing/serializers.py
from rest_framework import serializers
from .models import Section, Service, SuccessCase, ContactMessage, SelfAssessment

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class SuccessCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessCase
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        extra_kwargs = {
            'email': {'required': True},
            'message': {'min_length': 20}
        }

class SelfAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfAssessment
        fields = '__all__'