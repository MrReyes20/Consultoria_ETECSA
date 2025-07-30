from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet) # Ruta para /api/users/

urlpatterns = [
    path('', include(router.urls)),
]
