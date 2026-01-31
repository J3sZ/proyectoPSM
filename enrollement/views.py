# enrollment/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from planning.models import Term, Section
from .services import perform_enrollment

@login_required
def student_dashboard(request):
    """Pantalla principal del alumno: ve sus materias inscritas actuales"""
    student = request.user.student # Asumiendo que existe la relación OneToOne
    current_term = Term.objects.filter(is_active=True).first()
    
    my_enrollments = []
    if current_term:
        my_enrollments = student.enrollment_set.filter(section__term=current_term)

    return render(request, 'dashboard.html', {
        'student': student,
        'enrollments': my_enrollments,
        'term': current_term
    })

@login_required
def academic_offer(request):
    """Muestra todas las secciones disponibles para inscribir"""
    student = request.user.student
    current_term = Term.objects.filter(is_active=True).first()
    
    if not current_term:
        messages.error(request, "No hay un periodo académico activo.")
        return redirect('dashboard')

    # Filtramos las secciones:
    # 1. Del periodo actual
    # 2. De la carrera del estudiante
    available_sections = Section.objects.filter(
        term=current_term,
        subject__career=student.career
    ).order_by('subject__semester', 'subject__name')

    return render(request, 'offer.html', {
        'sections': available_sections,
        'term': current_term
    })

@login_required
def enroll_section(request, section_id):
    """Procesa la acción de inscribir (Solo POST)"""
    if request.method == 'POST':
        section = get_object_or_404(Section, id=section_id)
        student = request.user.student

        try:
            # Llamamos a nuestro servicio de validación lógica
            perform_enrollment(student, section)
            messages.success(request, f"¡Inscrito en {section.subject.name} correctamente!")
        
        except ValidationError as e:
            # Si falla alguna validación (cupos, prelación), mostramos el error
            messages.error(request, str(e.message)) # .message si es un solo error
        
        except Exception as e:
            messages.error(request, "Ocurrió un error inesperado.")

    # Siempre volvemos a la lista de oferta
    return redirect('academic_offer')

@login_required
def drop_section(request, enrollment_id):
    """Opción para retirar materia"""
    if request.method == 'POST':
        enrollment = get_object_or_404(request.user.student.enrollment_set, id=enrollment_id)
        enrollment.delete() # O cambiar status a 'RETIRADA'
        messages.warning(request, "Materia retirada.")
    
    return redirect('dashboard')