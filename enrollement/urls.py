# enrollment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('oferta/', views.academic_offer, name='academic_offer'),
    path('inscribir/<int:section_id>/', views.enroll_section, name='enroll_section'),
    path('retirar/<int:enrollment_id>/', views.drop_section, name='drop_section'),
]