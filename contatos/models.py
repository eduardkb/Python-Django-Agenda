from django.db import models
from django.utils import timezone

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    # funçao para mostrar corretamente no site admin o modelo
    # se nao tiver, mostra o objeto.
    def __str__(self):
        return self.nome

class Contato(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)
    # o upload_to cria pastas para ano, mes e dia da forma que esta abaixo
    foto = models.ImageField(blank=True, upload_to='fotos/%Y/%m/%d')

    # funçao para mostrar corretamente no site admin o modelo
    # se nao tiver, mostra o objeto.
    def __str__(self):
        return self.nome
