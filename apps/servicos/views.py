from django.shortcuts import render  # Importa a função render do Django, usada para renderizar templates HTML.

# Define uma função de visualização (view) chamada `lista_servicos`.
# Essa função será responsável por lidar com as requisições HTTP e retornar uma resposta.
def lista_servicos(request):
    """Lista de Combustíveis e Serviços"""
    
    # Cria uma lista de dicionários chamada `servicos`.
    # Cada dicionário representa um serviço ou combustível, contendo informações como nome, preço e descrição.
    servicos = [
        {'nome': 'Gasolina Aditivada', 'preco': 'R$ 6,50/L', 'descricao': 'Melhor desempenho e limpeza.'},
        {'nome': 'Etanol', 'preco': 'R$ 4,20/L', 'descricao': 'Opção mais ecológica.'},
        {'nome': 'Diesel S10', 'preco': 'R$ 5,80/L', 'descricao': 'Baixo teor de enxofre.'},
        {'nome': 'Troca de Óleo', 'preco': 'A partir de R$ 90,00', 'descricao': 'Serviço rápido e de confiança.'},
    ]
    
    # Renderiza o template HTML localizado em 'servicos/lista_servicos.html'.
    # Passa a lista de serviços como contexto para o template, permitindo que os dados sejam exibidos dinamicamente.
    return render(request, 'servicos/lista_servicos.html', {'servicos': servicos})
