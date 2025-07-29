from django.urls import path
from .views import UserCreateView, CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]