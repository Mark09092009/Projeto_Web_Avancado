from django.shortcuts import render, redirect  # Importa a função render, usada para exibir páginas HTML.
from django.contrib.auth.forms import UserCreationForm # Importa o formulário base do Django
from django.contrib import messages
from django.contrib.auth import login # Opcional: faz login automaticamente após o cadastro


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
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            # 2. Se a validação for OK, salva o novo usuário no banco de dados
            user = form.save()
            
            # Redireciona para o login ou faz login automático
            login(request, user) 
            messages.success(request, f"Conta criada com sucesso para {user.username}!")
            return redirect('home') # Redireciona para sua URL 'home' após o cadastro
        
        # 3. Se não for válido, o código continua e renderiza o form com os erros
        
    else:
        # 4. Se for um GET (primeira visita), exibe um formulário vazio
        form = UserCreationForm()
    
    # Renderiza o template, passando o objeto 'form'
    return render(request, 'registration/register.html', {'form': form})
