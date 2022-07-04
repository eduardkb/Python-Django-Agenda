from django.contrib import admin
from .models import Categoria, Contato

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email',
                    'data_criacao', 'categoria', 'mostrar')
    # por padrao só o primeiro campo é um link
    # item abaixo poe link em todos os campos na lista
    list_display_links = ('nome', 'sobrenome')

    # cria um filtro do lado direito da pagina
    list_filter = ('categoria', 'nome', 'sobrenome')

    # exibe x itens por pagina (padrao = 100)
    list_per_page = 20

    # inlui search
    search_fields = ('nome', 'sobrenome', 'telefone')

    # altera itens na lista para editaveis
    list_editable = ('telefone', 'mostrar')

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)

