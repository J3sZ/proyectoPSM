from django.db import models
from django.conf import settings # Para referenciar al usuario correctamente

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Comentario o Sugerencia")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post de {self.author.username} - {self.created_at.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-created_at'] # Los más nuevos primero