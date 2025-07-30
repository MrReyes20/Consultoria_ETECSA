
from django.db import models

from core import settings


class Section(models.Model):
    app_label = 'landing'
    SECTION_TYPES = (
        ('about', '¿Quiénes somos?'),
        ('services', 'Líneas de Servicios'),
        ('contact', 'Contactos'),
    )
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='sections/', null=True, blank=True)

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # Ej: 'fa-chart-line'

class SuccessCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    client_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='success_cases/')

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SelfAssessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    questions = models.JSONField()  # Almacena preguntas en formato JSON

class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey(SelfAssessment, on_delete=models.CASCADE)
    question_text = models.TextField()
    options = models.JSONField()  # {"A": "Opción 1", "B": "Opción 2"}

class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    question = models.ForeignKey(AssessmentQuestion, on_delete=models.CASCADE)
    response = models.CharField(max_length=1)  # 'A', 'B', etc.