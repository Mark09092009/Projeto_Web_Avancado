from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages 
from django.contrib.auth import login 
from django import forms 
from django.contrib.auth.forms import AuthenticationForm 
from django.utils.translation import gettext_lazy as _ 
from .forms import CustomUserCreationForm 
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContatoForm
from django.conf import settings

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("E-mail"), 
        max_length=254, 
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}) 
    )
    password = forms.CharField(
        label=_("Senha"), 
        strip=False, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}) 
    )

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