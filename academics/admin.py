from django.contrib import admin
from .models import Career, Subject, Prerequisite

# Esto permite editar las prelaciones DENTRO de la pantalla de la materia
class PrerequisiteInline(admin.TabularInline):
    model = Prerequisite
    fk_name = 'subject' # Indica que estamos editando desde el lado de la materia "hija"
    extra = 1 # Muestra 1 fila vacía para agregar rápido

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'career', 'semester', 'UC']
    list_filter = ['career', 'semester']
    search_fields = ['name', 'code']
    inlines = [PrerequisiteInline] # <--- Aquí conectamos el Inline

class CareerAdmin(admin.ModelAdmin):
    list_display = ['name','code']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Career, CareerAdmin)
# No hace falta registrar Prerequisite por separado si usas el Inline, 
# pero puedes hacerlo si quieres ver la tabla cruda.