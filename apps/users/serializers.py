# apps/users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'user_type', 'phone', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}, # La contraseña solo se escribe, no se lee
            'email': {'required': True},
            'username': {'required': True},
            'user_type': {'required': False} # Puede ser opcional al crear, o tener un valor por defecto
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
