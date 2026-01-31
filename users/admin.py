from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student

# 1. Configuración del Usuario Custom
class CustomUserAdmin(UserAdmin):
    # Agregamos tus campos nuevos a los 'fieldsets' (el formulario de edición)
    fieldsets = UserAdmin.fieldsets + (
        ('Roles Académicos', {'fields': ('is_student', 'is_teacher')}),
    )
    list_display = ['username', 'email', 'is_student', 'is_teacher', 'is_active']
    list_filter = ['is_student', 'is_teacher', 'is_staff']

# 2. Configuración del Estudiante
class StudentAdmin(admin.ModelAdmin):
    list_display = ['code', 'get_full_name', 'career', 'entry_date']
    search_fields = ['code', 'user__first_name', 'user__last_name']
    list_filter = ['career', 'entry_date']

    # Un helper para mostrar el nombre desde la relación con User
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nombre Completo'

admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)