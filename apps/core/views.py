from django.shortcuts import render, redirect  # Importa a função render, usada para exibir páginas HTML.
from django.contrib.auth.forms import UserCreationForm # Importa o formulário base do Django
from django.contrib import messages
from django.contrib.auth import login # Opcional: faz login automaticamente após o cadastro
from django.shortcuts import render, redirect
from django.contrib import messages
# IMPORTANTE: Mude a importação para o seu formulário personalizado!
from .forms import CustomUserCreationForm # Certifique-se de que a importação esteja correta
# ... (outras importações)


def home(request):
    """Página Inicial"""
    # Quando o usuário acessa a rota da página inicial (ex: '/'), 
    # o Django renderiza o arquivo 'core/home.html' e envia o título como contexto.
    return render(request, 'core/home.html', {
        'titulo': 'Posto Lucas - Seu Combustível com Qualidade'
    })

def sobre(request):
    """Página Sobre Nós"""
    # Quando o usuário acessa a rota 'sobre/', 
    # o Django renderiza o arquivo 'core/sobre.html' com o título correspondente.
    return render(request, 'core/sobre.html', {
        'titulo': 'Sobre Nós'
    })

def register(request):
    """Página Cadastro"""
    if request.method == 'POST':
        # 1. Se for um POST, preenche o formulário com os dados enviados
        form = CustomUserCreationForm(request.POST) # <-- Mudança aqui!
        
        if form.is_valid():
            # 2. Se a validação for OK, salva o novo usuário (com o email)
            user = form.save()
            
            # Redireciona para o login ou faz login automático
            login(request, user) 
            messages.success(request, f"Conta criada com sucesso para {user.username}!")
            return redirect('home')
        
    else:
        # 4. Se for um GET (primeira visita), exibe um formulário vazio
        form = CustomUserCreationForm() # <-- Mudança aqui!
    
    # Renderiza o template, passando o objeto 'form'
    return render(request, 'registration/register.html', {'form': form})
