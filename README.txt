"""
    pip install django
    pip install pillow  (por causa da importação de imagem)

    UNAPPLIED MIGRATIONS
        sao migracoes criadas na base de dados definida no
        proj/settings - DATABASES

        para migrar
            python manage.py migrate

        no arquivo models do application cria os campos das tabelas da DB.
        quando criar ou alterar tabela precisa executar o makemigrations
        daí para atualizar o migrations:
            python manage.py makemigrations
        e tem que atualizar o migrations
            Isso tudo cria as tabelas no banco de dados

   AREA ADMINISTRATIVA DO DJANGO
        ROOT access to admin area
        para acessar <local>/admin precisa criar uma ID
            python manage.py createsuperuser
                criado como eduard/123456

            Ja da pra acessar e fazer o management dos usuarios

        para incluir os models na area administrativa
            no <APP>/admin
                from .models import Categoria, Contato
                admin.site.register(Categoria)

            no <APP>/

    LISTANDO DADOS DA DB NA PAGINA
        na <APP>/views importa a classe
            from .models import Contato

            também no render passa um terceiro argumento. um dicionario
            com todos os campos da classe Contato
                {'contatos': contatos}

            no html do APP (index.html) itera com um for sobre contatos
                {% for contato in contatos %}
                {{ contato.sobrenome }}
                {% endfor %}

    TRATANDO ERRO
        primeira forma
            modificado no <APP>/views
                from django.http import Http404
                try
                except
                raise Http404

        segunda forma mais simples
            from django.shortcuts import get_object_or_404
            contato = get_object_or_404(Contato, id=contato_id)

    CONDICIONAL
        implementado no index.html com o contatos.mostrar
        if

    PAGINAÇAO
        implementado no app/views
            from django.core.paginator import Paginator
            e no index.html

    ORDENAR E FILTRAR
        no app/views
            contatos = Contato.objects.order_by('-id').filter(mostrar=True)

    CAMPO DE PESQUISA
        codigo html no contatos/index.html
            chama o endereço busca no action
        por isso criado o busca no url e funçao busca no views
            criado o html busca.html no app/templates/contatos
        Inteligencia da pesquisa esta no app/views funcao pesquisa

    CAMPO DE IMAGEM NO CONTATO
        tem q instalr o pillow
            pip install pillow

        quando o site trabalhar com imagem, no projeto/urls/
        precisa incluir:
            from django.conf import settings
            from django.conf.urls.static import static

            e depois do URLPATTERNS:
                + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

            no projeto/setings:
                MEDIA_ROOT = (BASE_DIR, 'media')
                MEDIA_URL = 'media/'

            criado o campo foto no app/models

            upload a foto no portal admin

            para mostrar a foto modificado o ver_contato.html

    MENSAGEM DE ERRO
        no arquivo parcial _messages.html para
        poder ser reutilizado em qqr lugar

    MUDANDO LINGUAGEM PADRAO DA AREA ADMINISTRATIVA
        no arquivo prj/settings.py tem por padrao:
            LANGUAGE_CODE = 'en-us'
            TIME_ZONE = 'UTC'

            para alterar para Brasil
                LANGUAGE_CODE = 'pt-BR'
                TIME_ZONE = 'America/Sao_Paulo'

            alemanha:
                LANGUAGE_CODE = 'de'
                TIME_ZONE = 'Europe/Berlin'

        o timezone prcisa alterar pois sempre quando pega hora atual,
        pega UTC se nao alterar

    CADASTRO DE USUARIOS
        feito no app accounts
            codigo no views, urls, e cadastro.html

    CRIAR FORMULARIO COM DJANGO
        Modificado arquivos
            contatos/models
            /views
            /dashboard

    COLETANDO ARQUIVOS ESTATICOS PARA FAZER O DEPLOY
        para o comando coletar tudo no projeto/settings.py
        tem que estar apontado para todos os arquivos estaticos:
            STATICFILES_DIRS = [os.path.join(BASE_DIR, "templates/static")]
        no arquivo settings.py do projeto:
            STATIC_ROOT = os.path.join('static')
        ai executa
            python manage.py collectstatic

"""