from django.shortcuts import render, redirect  # Importa funções para renderizar templates e redirecionar URLs.
from django.contrib.auth.forms import UserCreationForm  # Importa o formulário padrão de criação de usuário do Django.
from django.contrib import messages  # Permite exibir mensagens temporárias ao usuário.
from django.contrib.auth import login  # Função para autenticar e logar o usuário automaticamente.
from django import forms  # Importa ferramentas para criar e manipular formulários.
from django.contrib.auth.forms import AuthenticationForm  # Formulário padrão de autenticação do Django.
from django.utils.translation import gettext_lazy as _  # Permite traduzir textos para diferentes idiomas.
from .forms import CustomUserCreationForm  # Importa um formulário personalizado para criação de usuários.

# Classe personalizada para autenticação via e-mail.
class EmailAuthenticationForm(AuthenticationForm):
    """
    Substitui o rótulo 'Username' por 'E-mail' no formulário de login.
    Mantém o nome interno do campo como 'username' para compatibilidade com o backend padrão do Django.
    """
    username = forms.CharField(
        label=_("E-mail"),  # Define o rótulo como 'E-mail'.
        max_length=254,  # Limita o número máximo de caracteres.
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})  # Usa um widget de entrada de e-mail com classes CSS.
    )
    password = forms.CharField(
        label=_("Senha"),  # Define o rótulo como 'Senha'.
        strip=False,  # Permite que espaços sejam considerados na senha.
        widget=forms.PasswordInput(attrs={'class': 'form-control'})  # Usa um widget de entrada de senha com classes CSS.
    )

# Função para renderizar a página inicial.
def home(request):
    """
    Renderiza a página inicial do site.
    Envia um contexto com o título da página para o template 'core/home.html'.
    """
    return render(request, 'core/home.html', {
        'titulo': 'Posto Lucas - Seu Combustível com Qualidade'
    })

# Função para renderizar a página "Sobre Nós".
def sobre(request):
    """
    Renderiza a página 'Sobre Nós'.
    Envia um contexto com o título da página para o template 'core/sobre.html'.
    """
    return render(request, 'core/sobre.html', {
        'titulo': 'Sobre Nós'
    })

# Função para lidar com o cadastro de novos usuários.
def register(request):
    """
    Exibe o formulário de cadastro e processa os dados enviados.
    """
    if request.method == 'POST':  # Verifica se o método da requisição é POST (envio de dados).
        form = CustomUserCreationForm(request.POST)  # Preenche o formulário com os dados enviados.
        
        if form.is_valid():  # Verifica se os dados enviados são válidos.
            user = form.save()  # Salva o novo usuário no banco de dados.
            login(request, user)  # Faz login automático do usuário recém-cadastrado.
            messages.success(request, f"Conta criada com sucesso para {user.username}!")  # Exibe uma mensagem de sucesso.
            return redirect('home')  # Redireciona o usuário para a página inicial.
    else:
        form = CustomUserCreationForm()  # Cria um formulário vazio para exibição inicial.

    # Renderiza o template de registro, passando o formulário como contexto.
    return render(request, 'registration/register.html', {'form': form})
