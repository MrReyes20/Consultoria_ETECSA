# apps/users/views.py

from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer

CustomUser = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id') # Asegúrate de ordenar para consistencia
    serializer_class = CustomUserSerializer
    # Solo los administradores pueden gestionar usuarios
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        # Permite a los administradores ver todos los usuarios, pero los usuarios normales solo su propio perfil
        if self.action in ['retrieve', 'update', 'partial_update'] and not self.request.user.is_staff:
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset

    def perform_create(self, serializer):
        # Al crear un usuario, si no se especifica un user_type y el usuario que crea es admin, se puede asignar un default
        # O se puede requerir que el admin siempre especifique el user_type
        user = serializer.save()
        # Añadir lógica adicional aquí

    def perform_update(self, serializer):
        # Lógica para actualizar el usuario
        serializer.save()

    def perform_destroy(self, instance):
        # Lógica para eliminar el usuario
        instance.delete()
