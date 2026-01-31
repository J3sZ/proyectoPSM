from django.db import models

# Create your models here.

class Enrollment(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    section = models.ForeignKey('planning.Section', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('INSCRITA', 'Inscrita'), ('RETIRADA', 'Retirada')])
    
    # Campos académicos futuros
    final_grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        # Un estudiante no puede inscribir la misma sección dos veces
        unique_together = ('student', 'section') 

    def save(self, *args, **kwargs):
        # Aquí llamarías a las validaciones antes de guardar
        # self.clean() 
        super().save(*args, **kwargs)