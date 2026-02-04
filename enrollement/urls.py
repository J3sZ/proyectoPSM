# enrollment/urls.py
from django.urls import path
from . import views
from users import views as user_views # Importamos views de users para el registro
from .views import student_dashboard, academic_offer, enroll_section, drop_section

urlpatterns = [
    path('dashboard/', student_dashboard, name='dashboard'),
    path('oferta/', academic_offer, name='academic_offer'),
    path('register/', user_views.register, name='register'),
    path('inscribir/<int:section_id>/', enroll_section, name='enroll_section'),
    path('retirar/<int:enrollment_id>/', views.drop_section, name='drop_section'),
]