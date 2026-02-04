from django.db import models

# planning/models.py
class Term(models.Model): # Periodo Académico (ej. 2026-1)
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False) # Solo uno activo a la vez

    def __str__(self):
        return self.name

class Section(models.Model):
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    code = models.CharField(max_length=5) # Ej: "47xxxx""
    teacher = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    quota = models.IntegerField(default=40) # Cupos máximos
    schedule_data = models.JSONField() # Ej: {"Lunes": "08:00-10:00", "Miercoles": "08:00-10:00"}

    def enrolled_count(self):
        return self.enrollment_set.count() # Cuenta inscritos usando reverse relationship

    def has_space(self):
        return self.enrolled_count() < self.quota

    def __str__(self):
        return f"{self.subject.name} - Secc {self.code}"