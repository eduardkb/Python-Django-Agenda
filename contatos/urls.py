from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # o primeiro argumento abaixo é um argumento dinamico com tags html
    # para passar o id do contato pela url
    path('<int:contato_id>', views.ver_contato, name='ver_contato'),
    path('busca/', views.busca, name='busca'),
]
