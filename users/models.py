
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('consultant', 'Consultor'),
        ('client', 'Cliente'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.email