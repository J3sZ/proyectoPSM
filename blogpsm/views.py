from django.shortcuts import render



# enrollment/views.py (ACTUALIZAR)
from django.shortcuts import render
from blogpsm.models import Post # <--- Importar el modelo del blog
from blogpsm.forms import PostForm # <--- Importar el formulario

def home(request):
    """
    Página de inicio con Blog integrado.
    """
    # 1. Traer todos los posts ordenados
    posts = Post.objects.all()
    
    # 2. Preparar el formulario (solo si queremos mostrarlo vacío)
    form = PostForm()

    return render(request, 'home.html', {
        'posts': posts,
        'form': form
    })

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "¡Tu comentario ha sido publicado!")
    
    # Redirigir siempre a la página desde donde vino (el home)
    return redirect('home')

@login_required
def edit_post(request, post_id):
    # Buscamos el post o damos error 404
    post = get_object_or_404(Post, id=post_id)

    # SEGURIDAD: Si el usuario actual NO es el dueño del post, prohibimos la entrada
    if post.author != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este comentario.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post) # 'instance' carga los datos viejos
        if form.is_valid():
            form.save()
            messages.success(request, "Comentario actualizado.")
            return redirect('home')
    else:
        form = PostForm(instance=post) # Cargar formulario con datos existentes

    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # SEGURIDAD: Solo el dueño puede borrar
    if post.author != request.user:
        messages.error(request, "No puedes borrar un comentario que no es tuyo.")
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Comentario eliminado correctamente.")
    
    return redirect('home')