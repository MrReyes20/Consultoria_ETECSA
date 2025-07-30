# apps/landing/serializers.py

from rest_framework import serializers
from .models import Section, Service, SuccessCase, ContactMessage, SelfAssessment, AssessmentQuestion, Post, Comment

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

class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = '__all__'
        read_only_fields = ['assessment'] # La evaluación se asignará al crear/actualizar desde SelfAssessment

class SelfAssessmentSerializer(serializers.ModelSerializer):
    # Permite la creación y actualización anidada de preguntas junto con la autoevaluación
    questions = AssessmentQuestionSerializer(many=True, required=False)

    class Meta:
        model = SelfAssessment
        fields = '__all__'

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        self_assessment = SelfAssessment.objects.create(**validated_data)
        for question_data in questions_data:
            AssessmentQuestion.objects.create(assessment=self_assessment, **question_data)
        return self_assessment

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Eliminar preguntas existentes que no están en los datos de actualización
        existing_questions_ids = [q.get('id') for q in questions_data if 'id' in q]
        for question in instance.questions.all():
            if question.id not in existing_questions_ids:
                question.delete()

        # Crear o actualizar preguntas
        for question_data in questions_data:
            question_id = question_data.get('id', None)
            if question_id:
                # Actualizar pregunta existente
                question = AssessmentQuestion.objects.get(id=question_id, assessment=instance)
                question.question_text = question_data.get('question_text', question.question_text)
                question.options = question_data.get('options', question.options)
                question.save()
            else:
                # Crear nueva pregunta
                AssessmentQuestion.objects.create(assessment=instance, **question_data)
        return instance

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username') # Muestra el nombre de usuario del autor

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'published_date', 'updated_date', 'slug'] # El slug se genera automáticamente

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post', 'created_at'] # El post se asigna al crear, la fecha es auto
