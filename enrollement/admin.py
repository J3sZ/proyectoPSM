from django.contrib import admin
from .models import Enrollment

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'section', 'status', 'created_at', 'final_grade']
    list_filter = ['status', 'section__term', 'section__subject'] # Filtros potentes
    search_fields = ['student__code', 'student__user__username', 'section__subject__name']
    date_hierarchy = 'created_at' # Navegación por fechas arriba del admin

admin.site.register(Enrollment, EnrollmentAdmin)