from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, StudentUser, TeacherUser

# 1. Configuración del Usuario Custom
class CustomUserAdmin(UserAdmin):
    # Agregamos tus campos nuevos a los 'fieldsets' (el formulario de edición)
    fieldsets = UserAdmin.fieldsets + (
        ('Roles Académicos', {'fields': ('is_student', 'is_teacher')}),
    )
    list_display = ['username', 'email', 'is_student', 'is_teacher', 'is_active']
    list_filter = ['is_student', 'is_teacher', 'is_staff']

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Perfil Académico'
    fk_name = 'user'

# --- 2. Admin para Estudiantes ---
class StudentUserAdmin(UserAdmin):
    inlines = [StudentInline] # <--- Pegamos el perfil aquí
    list_display = ('username', 'email', 'get_student_code', 'get_career', 'is_active')
    
    # Filtramos para que en esta lista SOLO salgan estudiantes
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_student=True)

    # Cuando creamos uno nuevo, forzamos que sea is_student=True
    def save_model(self, request, obj, form, change):
        obj.is_student = True
        super().save_model(request, obj, form, change)

    # Helpers para mostrar info en la tabla
    def get_student_code(self, obj):
        # Intentamos obtener el carnet, si no existe (aún) devolvemos guión
        return obj.student.code if hasattr(obj, 'student') else '-'
    get_student_code.short_description = 'Carnet'

    def get_career(self, obj):
        return obj.student.career if hasattr(obj, 'student') else '-'
    get_career.short_description = 'Carrera'

# --- 3. Admin para Profesores ---
class TeacherUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    
    # Filtramos para que SOLO salgan profesores
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_teacher=True)

    # Cuando creamos uno nuevo, forzamos que sea is_teacher=True
    def save_model(self, request, obj, form, change):
        obj.is_teacher = True
        super().save_model(request, obj, form, change)

# --- 4. Registro ---
# Registramos los modelos Proxy, NO el User base (para no confundir)
admin.site.register(StudentUser, StudentUserAdmin)
admin.site.register(TeacherUser, TeacherUserAdmin)