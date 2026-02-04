
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('enrollement.urls')),
    path('', include('blogpsm.urls')),
    
    # --- SISTEMA DE LOGIN ---
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # Para el logout, usamos next_page para asegurar que vaya al login de nuevo
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
