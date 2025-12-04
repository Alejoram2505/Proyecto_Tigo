from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('ing', 'Ingeniero'),
        ('cliente', 'Cliente'),
    )
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cliente')

    def __str__(self):
        return f"{self.username} ({self.rol})"

