from django.shortcuts import render  # Importa a função render, usada para exibir páginas HTML.

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
