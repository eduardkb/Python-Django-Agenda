from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    # verificando se usuario e senha estao corretos
    user = auth.authenticate(request, username=usuario, password=senha)

    # user retorna NONE se nao corresponder credenciais
    if not user:
        messages.error(request, 'Usuario ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Usuario logado!!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    messages.info(request, 'Usuario deslogado.')
    return redirect('login')


def cadastro(request):
    # verificar se usuario esta autenticado
    print(f"Is User authenticated? {request.user.is_authenticated}")
    if not request.user.is_authenticated:
        print("No user logged in!!!")
        messages.info(request, "Nenhum usuário logado. Logue para acessar o cadastro de usuários.")
        return redirect('login')


    # get post message and print
    sMsg = request.POST
    # messages.success(request, 'Olá Mundo!!!')
    # messages.info(request, f'POST MESSAGE: {sMsg}')
    print("###############################")
    print(f'POST MESSAGE: {sMsg}')
    print("###############################")

    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    # verificar se algo esta vazio
    if not nome or not sobrenome or not email or not usuario \
            or not senha or not senha2:
        messages.error(request, "Nada cadastrado. Todos os campos sao obrigatórios.")
        return render(request, 'accounts/cadastro.html')

    # verificar e-mail
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/cadastro.html')

    # verificar se usuario tem pelo menos 6 caracteres
    if len(usuario) < 6:
        messages.error(request, 'Usuário inválido. Precisa ter pelo menos 6 caracteres.')
        return render(request, 'accounts/cadastro.html')

    # verificar tamanho da senha
    if len(senha) < 6:
        messages.error(request, 'Senha inválida. Precisa ter pelo menos 6 caracteres.')
        return render(request, 'accounts/cadastro.html')

    # verificar se as senhas sao iguais
    if senha != senha2:
        messages.error(request, 'As duas senhas digitadas nao sao iguais.')
        return render(request, 'accounts/cadastro.html')

    # verificar se e-mail e usuario ja nao estao cadastrados
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário ja existe.')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email ja existe.')

    messages.success(request, 'Usuário registrado com sucesso. Faça login.')

    # salvar usuario na DB
    user = User.objects.create_user(username=usuario, email=email, password=senha,
                                    first_name=nome, last_name=sobrenome)
    user.save()

    # redireciona para pagina de login
    return redirect('login')


# decorador para nao ir para a pagina sem estar logado.
# se nao estiver logado redireciona para a pagina login
# @login_required(redirect_field_name='login')
def dashboard(request):

    # verificar depois de entrar na funçao para mostrar mensagem quando nao autenticado
    print(f"Is User authenticated? {request.user.is_authenticated}")
    if not request.user.is_authenticated:
        print("No user logged in!!!")
        messages.info(request, "Nenhum usuário logado. Logue para acessar o dashboard.")
        return redirect('login')

    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulario')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    # verifica se descriçao é valida
    descricao = request.POST.get('descricao')
    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais de 5 caracteres.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    # salvar o contato
    form.save()
    messages.success(request, f"Cadastro de '{request.POST.get('nome')}' efetuado com sucesso.")

    # retorna para a pagina dashboard
    return redirect('dashboard')
