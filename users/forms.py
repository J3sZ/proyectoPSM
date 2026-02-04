# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Student
from academics.models import Career # Importamos las carreras para el select

class StudentRegistrationForm(UserCreationForm):
    # Campos extra que no están en el modelo User base
    first_name = forms.CharField(label="Nombre", max_length=100, required=True)
    last_name = forms.CharField(label="Apellido", max_length=100, required=True)
    email = forms.EmailField(label="Correo Electrónico", required=True)
    
    # Campos específicos del Estudiante
    code = forms.CharField(
        label="Número de Carnet / Matrícula", 
        max_length=20,
        help_text="Ej: 2026-00123"
    )
    career = forms.ModelChoiceField(
        queryset=Career.objects.all(),
        label="Carrera a cursar",
        empty_label="Seleccione su carrera",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    @transaction.atomic
    def save(self, commit=True):
        # 1. Guardamos el Usuario base (User) pero sin escribir en BD aún
        user = super().save(commit=False)
        
        # Asignamos los datos del formulario al objeto usuario
        user.is_student = True  # ¡CRUCIAL! Marcarlo como estudiante
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save() # Guardamos el User en la BD

            # 2. Guardamos el Perfil de Estudiante (Student)
            from django.utils import timezone
            Student.objects.create(
                user=user,
                code=self.cleaned_data['code'],
                career=self.cleaned_data['career'],
                entry_date=timezone.now() # Fecha de ingreso automática
            )
        
        return user