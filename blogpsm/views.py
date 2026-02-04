from django.shortcuts import render



def home(request):
    """
    Página de inicio pública.
    Si el usuario ya está logueado, lo manda al dashboard directo.
    """
    # if request.user.is_authenticated:
    #     if hasattr(request.user, 'student'):
    #         return redirect('dashboard')
    #     # Si es profesor o admin, podrías redirigir a otro lado
    #     # return redirect('admin:index') 
    
    return render(request, 'home.html')
