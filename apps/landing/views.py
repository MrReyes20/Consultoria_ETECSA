# apps/landing/views.py

from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.utils.text import slugify
from apps.users.permissions import IsConsultantOrAdmin, IsOwnerOrConsultant, IsAdminOnly

from . import serializers
from .models import (Section, Service, SuccessCase, ContactMessage, 
                     SelfAssessment, AssessmentQuestion, UserResponse, 
                     AssessmentResult, Post, Comment)
from .serializers import (
    SectionSerializer,
    ServiceSerializer,
    SuccessCaseSerializer,
    ContactMessageSerializer,
    SelfAssessmentSerializer,
    AssessmentQuestionSerializer,
    UserResponseSerializer,
    AssessmentResultSerializer,
    PostSerializer,
    CommentSerializer
)

# Vistas para el contenido público (solo lectura)
class PublicContentView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sections = Section.objects.all()
        services = Service.objects.all()
        success_cases = SuccessCase.objects.all()
        posts = Post.objects.filter(is_published=True).order_by('-published_date') # Solo posts publicados

        return Response({
            'sections': SectionSerializer(sections, many=True).data,
            'services': ServiceSerializer(services, many=True).data,
            'success_cases': SuccessCaseSerializer(success_cases, many=True).data,
            'blog_posts': PostSerializer(posts, many=True).data
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

class UserResponseCreateView(generics.CreateAPIView):
    serializer_class = UserResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AssessmentResultCreateView(generics.CreateAPIView):
    serializer_class = AssessmentResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Verificar si ya existe un resultado para este usuario y evaluación
        assessment = serializer.validated_data.get('assessment')
        existing_result = AssessmentResult.objects.filter(
            user=self.request.user,
            assessment=assessment
        ).first()

        if existing_result:
            # Actualizar el resultado existente
            existing_result.score = serializer.validated_data.get('score')
            existing_result.recommendations = serializer.validated_data.get('recommendations')
            existing_result.save()
            return existing_result

        serializer.save(user=self.request.user)

class UserAssessmentResultsView(generics.ListAPIView):
    serializer_class = AssessmentResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AssessmentResult.objects.filter(user=self.request.user)
    permission_classes = [permissions.AllowAny] # Las autoevaluaciones pueden ser públicas

# ViewSets para la gestión administrativa (requiere autenticación y permisos de administrador)

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAdminUser] # Solo administradores pueden gestionar secciones

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser] # Solo administradores pueden gestionar servicios

class SuccessCaseViewSet(viewsets.ModelViewSet):
    queryset = SuccessCase.objects.all()
    serializer_class = SuccessCaseSerializer
    permission_classes = [permissions.IsAdminUser] # Solo administradores pueden gestionar casos de éxito

class SelfAssessmentViewSet(viewsets.ModelViewSet):
    queryset = SelfAssessment.objects.all()
    serializer_class = SelfAssessmentSerializer
    permission_classes = [permissions.IsAdminUser] # Solo administradores pueden gestionar autoevaluaciones

class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    queryset = AssessmentQuestion.objects.all()
    serializer_class = AssessmentQuestionSerializer
    permission_classes = [permissions.IsAdminUser] # Solo administradores pueden gestionar preguntas

    def get_queryset(self):
        # Permite filtrar preguntas por autoevaluación si se pasa assessment_id en la URL
        assessment_id = self.kwargs.get('assessment_pk') # Si se usa anidación de URLs
        if assessment_id:
            return self.queryset.filter(assessment_id=assessment_id)
        return self.queryset

    def perform_create(self, serializer):
        # Si la pregunta se crea anidada, el assessment_id ya estará en el contexto
        # Si se crea directamente, se debe asegurar que se asocie a una evaluación existente
        if 'assessment_pk' in self.kwargs:
            assessment = SelfAssessment.objects.get(pk=self.kwargs['assessment_pk'])
            serializer.save(assessment=assessment)
        else:
            serializer.save()

# ViewSets para la gestión del Blog
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser] # Solo administradores pueden gestionar posts

    def perform_create(self, serializer):
        # Asigna el autor del post al usuario autenticado
        serializer.save(author=self.request.user, slug=slugify(serializer.validated_data['title']))

    def perform_update(self, serializer):
        # Actualiza el slug si el título cambia
        if 'title' in serializer.validated_data:
            serializer.validated_data['slug'] = slugify(serializer.validated_data['title'])
        serializer.save()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser] # Solo administradores pueden gestionar comentarios

    def get_queryset(self):
        # Permite filtrar comentarios por post si se pasa post_pk en la URL
        post_id = self.kwargs.get('post_pk') # Si se usa anidación de URLs
        if post_id:
            return self.queryset.filter(post_id=post_id)
        return self.queryset

    def perform_create(self, serializer):
        # Si el comentario se crea anidado, el post_id ya estará en el contexto
        # Si se crea directamente, se debe asegurar que se asocie a un post existente
        if 'post_pk' in self.kwargs:
            post = Post.objects.get(pk=self.kwargs['post_pk'])
            serializer.save(post=post)
        else:
            serializer.save() # Esto requeriría que el post_id se envíe en el body
