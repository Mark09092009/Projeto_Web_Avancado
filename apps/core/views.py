from django.shortcuts import render, redirect  # Importa funções para renderizar templates e redirecionar URLs.
from django.contrib.auth.forms import UserCreationForm  # Importa o formulário padrão de criação de usuário do Django.
from django.contrib import messages  # Permite exibir mensagens temporárias ao usuário.
from django.contrib.auth import login  # Função para autenticar e logar o usuário automaticamente.
from django import forms  # Importa ferramentas para criar e manipular formulários.
from django.contrib.auth.forms import AuthenticationForm  # Formulário padrão de autenticação do Django.
from django.utils.translation import gettext_lazy as _  # Permite traduzir textos para diferentes idiomas.
from .forms import CustomUserCreationForm  # Importa um formulário personalizado para criação de usuários.
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContatoForm
from django.conf import settings

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

def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST) 
        
        if form.is_valid():
            cleaned_data = form.cleaned_data 
            nome = cleaned_data['nome']
            email = cleaned_data['email']
            assunto = cleaned_data.get('assunto', 'Contato pelo Site (Sem Assunto)') 
            mensagem = cleaned_data['mensagem']

            # NOVIDADE: from_email agora é o e-mail do cliente, 
            # e recipient_list é o e-mail do posto.
            send_mail(
                subject=f'Contato do Site: {assunto} (De: {nome})', 
                message=f'Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}', 
                from_email=email, # O e-mail do cliente
                recipient_list=[settings.DEFAULT_FROM_EMAIL], # O e-mail do posto (o seu Gmail)
                fail_silently=False,
            )
            
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Em breve, entraremos em contato.')
            return redirect('home')
            
    else:
        # Se for um GET (primeira visita) ou falhar na validação
        form = ContatoForm()

    # CORREÇÃO: Passa sempre o objeto 'form' para o template.
    return render(request, 'core/contato.html', {'form': form})