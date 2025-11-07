from django.shortcuts import render  # Importa a função render do Django.

def lista_servicos(request):
    """Lista de Combustíveis e Serviços"""
    
    # Cria uma lista de dicionários, onde cada dicionário representa um serviço ou combustível.
    servicos = [
        {'nome': 'Gasolina Aditivada', 'preco': 'R$ 6,50/L', 'descricao': 'Melhor desempenho e limpeza.'},
        {'nome': 'Etanol', 'preco': 'R$ 4,20/L', 'descricao': 'Opção mais ecológica.'},
        {'nome': 'Diesel S10', 'preco': 'R$ 5,80/L', 'descricao': 'Baixo teor de enxofre.'},
        {'nome': 'Troca de Óleo', 'preco': 'A partir de R$ 90,00', 'descricao': 'Serviço rápido e de confiança.'},
    ]
    
    # Renderiza o template 'servicos/lista_servicos.html'
    # e envia a lista de serviços para o HTML exibir dinamicamente.
    return render(request, 'servicos/lista_servicos.html', {'servicos': servicos})
