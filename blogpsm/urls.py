from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('create_post', views.create_post, name='create_post'),
    path('editar/<int:post_id>/', views.edit_post, name='edit_post'),
    path('borrar/<int:post_id>/', views.delete_post, name='delete_post')
]