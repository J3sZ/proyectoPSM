from django.contrib import admin
from .models import Term, Section

class SectionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'term', 'teacher', 'quota', 'get_enrolled_count']
    list_filter = ['term', 'subject__career']
    search_fields = ['subject__name', 'code']
    
    # Para ver en el admin cuántos van inscritos
    def get_enrolled_count(self, obj):
        return obj.enrolled_count()
    get_enrolled_count.short_description = 'Inscritos'

class TermAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active']

admin.site.register(Section, SectionAdmin)
admin.site.register(Term, TermAdmin)