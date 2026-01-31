

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=20, unique=True, null= True)
    career = models.ForeignKey('academics.Career', on_delete=models.CASCADE)
    entry_date = models.DateField()

    def __str__(self):
        return f"{self.code} - {self.user.get_full_name()}"

class StudentUser(User):
    """Modelo Proxy para gestionar solo Estudiantes en el Admin"""
    class Meta:
        proxy = True # No crea tabla nueva
        verbose_name = 'Estudiante (Usuario)'
        verbose_name_plural = 'Estudiantes (Usuarios)'

class TeacherUser(User):
    """Modelo Proxy para gestionar solo Profesores en el Admin"""
    class Meta:
        proxy = True
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'

