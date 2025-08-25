# apps/landing/models.py

from django.db import models
from core import settings # Asegúrate de que esta importación sea correcta para tu estructura de proyecto

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

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # Ej: 'fa-chart-line'

    def __str__(self):
        return self.title

class SuccessCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    client_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='success_cases/')

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class SelfAssessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # questions = models.JSONField() # Se reemplaza por el modelo AssessmentQuestion

    def __str__(self):
        return self.title

class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey(SelfAssessment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    options = models.JSONField()  # {"A": "Opción 1", "B": "Opción 2"}

    def __str__(self):
        return f"{self.assessment.title} - {self.question_text[:50]}..."

class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    question = models.ForeignKey(AssessmentQuestion, on_delete=models.CASCADE)
    response = models.CharField(max_length=1)  # 'A', 'B', etc.

    def __str__(self):
        return f"Respuesta de {self.user.username if self.user else 'Anónimo'} a {self.question.question_text[:30]}..."

class AssessmentResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assessment = models.ForeignKey(SelfAssessment, on_delete=models.CASCADE)
    score = models.FloatField()  # Puntaje total
    recommendations = models.TextField()  # Recomendaciones basadas en el resultado
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resultado de {self.user.username} en {self.assessment.title}"

    class Meta:
        unique_together = ['user', 'assessment']

# Modelos para el Blog
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255) # Para URLs amigables
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_posts/', null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False) # Para moderación de comentarios

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comentario de {self.author_name} en {self.post.title[:30]}..."
