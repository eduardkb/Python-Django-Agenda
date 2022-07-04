from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages

# Create your views here.
def index(request):
    # exemplo de como mostrar mensagem
    # neste caso se ativo, sempre mostra a mensagem no index pois
    # nao verifica um erro ou problema
    # <<messages.add_message(request, messages.ERROR, 'Ocoreu um Erro')

    # ORIGINAL: mostrar todos os contatos com ordenaçao default:
    # contatos = Contato.objects.all()

    # recuperar os dados ordenando por nome
    # - na frente do campo ordena em ordem decrescente
    contatos = Contato.objects.order_by('nome')

    # recuperar os dados ordenando por ID
    # - na frente do campo ordena em ordem decrescente
    # também adiciona filtro (este filtro está duplicado com codigo if no index.html)
    # mas da para remover o if no index.html e só mostraria os com mostrar = true
    # contatos = Contato.objects.order_by('-id').filter(mostrar=True)

    # para criar o paginador:
    paginator = Paginator(contatos, 25)
    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })

# este contato_id vem como argumento do urls.py
def ver_contato(request, contato_id):
    # pega um contato só com o id = contato_id
    # Original(sem tratamento de erro):
    # contato = Contato.objects.get(id=contato_id)

    # 1a FORMA DE TRATAR ERRO
    # com tratamento de erro (pagina nao existe)
    contato = get_object_or_404(Contato, id=contato_id)

    # 2a FORMA DE TRATAR ERRO
    # verificar se pessoa pode ser exibida. se nao, raise exception
    if not contato.mostrar:
        raise Http404

    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })

def busca(request):
    termo = request.GET.get('termo')

    # sem o abixo se url terminar com /busca
    # da erro "ValueError at /busca/"
    if termo is None or not termo:
        # ORIGINAL que levanta uma esseçao
        # <<raise Http404

        # NOVO COM MENSAGEM NA PAGINA
        messages.add_message(request, messages.ERROR, 'Campo de pesquisa nao pode ficar vazio.')
        # para nao continuar o codigo e fazer a pesquisa com erro, redireciona para o index
        return redirect('index')
    # EXEMPLO DE PESQUISA 1
    # <<<contatos = Contato.objects.order_by('nome').filter(
        # somente nome procura nome exato
        # como abaixo procura nome parcial
        # consulta normal: (coloca and em tudo na query)
        # <<<nome__icontains=termo, sobrenome__icontains=termo

        # consulta alterada com a classe importada Q para
        # conseguir fazer 'and'
        # mas o abaixo na acha nome junto com sobrenome
        # pois a query faz nome ou sobrenome. nao preve os dois juntos
        # <<<Q(nome__icontains=termo) |
        # <<<Q(sobrenome__icontains=termo)
    # <<<)

    # EXEMPLO DE PESQUISA 2 (MAIS COMPLEXA)
    campos = Concat('nome', Value(' '), 'sobrenome')
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        # procura só nome, só sobrenome ou ambos juntos (campos)
        # nao precisa do Q se for só um campo
        Q(nome_completo__icontains=termo) |
        # | = ou
        # procura o telefone também
        Q(telefone__icontains=termo)
    )

    # mostra a consulta que é feita na base de dados
    print("############################################")
    print(contatos.query)
    print("############################################")

    paginator = Paginator(contatos, 25)
    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    if len(contatos) == 0:
        messages.add_message(request, messages.INFO, f'Nenhuma pessoa encontrada com a pesquisa: "{termo}"".')
        return redirect('index')
    else:
        messages.add_message(request, messages.SUCCESS, f'Pessoas abaixo foram encontradas com a pesquisa.')

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })
