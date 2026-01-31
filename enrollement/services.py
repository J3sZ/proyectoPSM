# enrollment/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Enrollment
from academics.models import Prerequisite

def validate_enrollment(student, section):
    """
    Verifica todas las reglas antes de inscribir.
    Retorna True si pasa, o lanza ValidationError si falla.
    """
    
    # 1. Validar si ya inscribió esta materia en este periodo (evitar duplicados)
    # Buscamos inscripciones del mismo estudiante, mismo periodo y misma materia
    already_enrolled = Enrollment.objects.filter(
        student=student,
        section__term=section.term,
        section__subject=section.subject
    ).exists()
    
    if already_enrolled:
        raise ValidationError(f"Ya has inscrito la materia {section.subject.name}.")

    # 2. Validar Cupos
    if not section.has_space():
        raise ValidationError("No hay cupos disponibles en esta sección.")

    # 3. Validar Prelaciones (La parte difícil)
    # Obtenemos los IDs de las materias que son requisito
    requirements = section.subject.requirements.all() # Usando el related_name que definimos antes
    
    for req in requirements:
        prereq_subject = req.prerequisite
        # Buscamos si el estudiante aprobó esa materia (nota > 10 o status 'APROBADO')
        # Asumiremos por ahora que existe un historial o buscamos en enrollments pasados
        has_passed = Enrollment.objects.filter(
            student=student,
            section__subject=prereq_subject,
            final_grade__gte=10 # Ejemplo: nota mínima 10
        ).exists()
        
        if not has_passed:
            raise ValidationError(f"No cumples con el pre-requisito: {prereq_subject.name}")

    # 4. Validar Choque de Horario (Simplificado)
    # Aquí compararías section.schedule_data con las otras secciones inscritas
    # ... lógica de horarios ...

    return True

def perform_enrollment(student, section):
    """Ejecuta la inscripción de forma atómica"""
    with transaction.atomic():
        validate_enrollment(student, section)
        
        # Crear la inscripción
        Enrollment.objects.create(
            student=student,
            section=section,
            status='INSCRITA'
        )