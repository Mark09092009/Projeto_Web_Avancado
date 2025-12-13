from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, ContatoForm, FuncionarioForm
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, 'core/home.html', {
        'titulo': 'Posto Lucas - Seu Combustível com Qualidade'
    })


def sobre(request):
    return render(request, 'core/sobre.html', {
        'titulo': 'Sobre Nós'
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Conta criada com sucesso para {user.username}!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def contato(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para enviar uma mensagem de contato.')
        return redirect('login')

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['email'] = request.user.email
        form = ContatoForm(post_data)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nome = cleaned_data['nome']
            email = cleaned_data['email']
            assunto = cleaned_data.get('assunto', 'Contato pelo Site (Sem Assunto)')
            mensagem = cleaned_data['mensagem']

            send_mail(
                subject=f'Contato do Site: {assunto} (De: {nome})',
                message=f'Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}',
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Em breve, entraremos em contato.')
            return redirect('home')
    else:
        form = ContatoForm()

    return render(request, 'core/contato.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def adicionar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso.')
            return redirect('home')
    else:
        form = FuncionarioForm()

    return render(request, 'core/add_funcionario.html', {'form': form, 'titulo': 'Adicionar Funcionário'})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_funcionario(request):
    """Permite que um superusuário registre um novo usuário e seu `Funcionario` associado."""
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        func_form = FuncionarioForm(request.POST)

        if user_form.is_valid() and func_form.is_valid():
            user = user_form.save()
            # por padrão, tornar o usuário criado como staff para poder acessar o admin se necessário
            user.is_staff = True
            user.save()

            funcionario = func_form.save(commit=False)
            funcionario.user = user
            funcionario.save()

            messages.success(request, 'Usuário e Funcionário cadastrados com sucesso.')
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
        func_form = FuncionarioForm()

    return render(request, 'registration/register_funcionario.html', {
        'user_form': user_form,
        'func_form': func_form,
        'titulo': 'Registrar Funcionário'
    })