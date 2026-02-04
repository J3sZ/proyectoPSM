from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from planning.models import Term, Section
from .models import Student
from enrollement.models import Enrollment # Importamos Enrollment de la app enrollement
from users.decorators import student_required
from enrollement.services import perform_enrollment # Importamos el servicio de validación de enrollement
from .forms import StudentRegistrationForm
from django.contrib.auth import login

def register(request):
    # Si ya está logueado, lo sacamos de aquí
    if request.user.is_authenticated:
        return redirect('dashboard') 

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # El form.save() ya maneja la creación del User y el Student
                user = form.save()
                
                # Logueamos al usuario inmediatamente
                login(request, user)
                
                messages.success(request, f"¡Bienvenido, {user.first_name}! Tu cuenta ha sido creada.")
                return redirect('dashboard')
            
            except Exception as e:
                # Esto atrapa errores como "Carnet duplicado"
                messages.error(request, "Error al registrar: Verifica que el carnet no esté ya registrado.")
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = StudentRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

@student_required
def student_dashboard(request):
    """
    Pantalla principal: Muestra el horario actual del alumno.
    """
    student = request.user.student
    
    # Buscamos el periodo activo (Ej. "2024-1")
    current_term = Term.objects.filter(is_active=True).first()
    
    my_enrollments = []
    if current_term:
        # Buscamos las inscripciones de este alumno en el periodo actual
        my_enrollments = Enrollment.objects.filter(
            student=student, 
            section__term=current_term
        ).select_related('section__subject', 'section__teacher') 
        # .select_related optimiza la base de datos para no hacer mil consultas

    return render(request, 'enrollment/dashboard.html', {
        'student': student,
        'enrollments': my_enrollments,
        'term': current_term
    })

@student_required
def academic_offer(request):
    """
    Pantalla de inscripción: Lista las secciones disponibles.
    """
    student = request.user.student
    current_term = Term.objects.filter(is_active=True).first()
    
    if not current_term:
        messages.warning(request, "No hay un periodo académico activo en este momento.")
        return redirect('dashboard')

    # Filtramos las secciones:
    # 1. Que sean del periodo actual
    # 2. Que pertenezcan a la carrera del estudiante
    # 3. Ordenamos por semestre y nombre de materia
    sections = Section.objects.filter(
        term=current_term,
        subject__career=student.career
    ).select_related('subject', 'teacher').order_by('subject__semester', 'subject__name')

    # Opcional: Podrías excluir aquí las que ya inscribió para que no salgan en la lista
    # pero a veces es mejor mostrarlas y que el botón diga "Inscrita".

    return render(request, 'enrollment/offer.html', {
        'sections': sections,
        'term': current_term
    })

@student_required
def enroll_section(request, section_id):
    """
    Procesa la inscripción (Solo acepta POST por seguridad).
    """
    if request.method == 'POST':
        section = get_object_or_404(Section, id=section_id)
        student = request.user.student

        try:
            # Llamamos al servicio que valida prelaciones, cupos y choques
            perform_enrollment(student, section)
            
            messages.success(request, f"¡Inscrito correctamente en {section.subject.name}!")
        
        except ValidationError as e:
            # Si falla alguna validación (ej. prelación), mostramos el error
            messages.error(request, e.message)
        
        except Exception as e:
            # Error inesperado (ej. base de datos caída)
            messages.error(request, "Ocurrió un error inesperado al procesar la solicitud.")
    
    # Siempre redirigimos a la oferta para que siga inscribiendo
    return redirect('academic_offer')

@student_required
def drop_section(request, enrollment_id):
    """
    Permite retirar una materia.
    """
    if request.method == 'POST':
        # Buscamos la inscripción asegurando que pertenezca al usuario actual (Seguridad)
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user.student)
        
        materia_nombre = enrollment.section.subject.name
        enrollment.delete() # O enrollment.status = 'RETIRADA' si prefieres historial
        
        messages.warning(request, f"Has retirado la materia {materia_nombre}.")
    
    return redirect('dashboard')
    
