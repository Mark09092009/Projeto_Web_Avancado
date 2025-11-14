"""
Definições de Rotas (URLs) para o Aplicativo 'gerenciamento'.

Este arquivo mapeia URLs específicas para as funções de visualização (views)
do Django. Ele é responsável por direcionar as requisições HTTP do usuário
para a lógica correta dentro do sistema de gestão do posto de combustível.

Convenções de Nomes:
- A variável principal é 'urlpatterns', uma lista de objetos 'path'.
- Cada 'path' define a rota (o que aparece no navegador), a view (a função Python que processa a requisição)
  e um nome único (usado para referência em templates e redirecionamentos, como no `redirect('nome_da_rota')`).
"""

from django.urls import path
from . import views

# Lista de rotas específicas do app 'gerenciamento'
urlpatterns = [
    # Rota principal de visualização e movimentação de estoque.
    # Conecta à view que exibe o status atual do estoque e o formulário de entrada/saída.
    path('estoque/', views.estoque_gasolina_view, name='estoque_gasolina'),

    # Rota para a configuração inicial.
    # Permite ao administrador adicionar novos tipos de combustível (Gasolina Comum, Etanol, etc.) ao sistema.
    path('estoque/adicionar/', views.adicionar_combustivel_view, name='adicionar_combustivel'),

    # Rota para a tela de edição de preços.
    # Usada para atualizar o preço de venda por litro de combustíveis e o preço unitário de serviços.
    path('combustiveis/editar/', views.edit_combustiveis_view, name='edit_combustiveis'), 

    # Rota para a gestão financeira.
    # Exibe o histórico de transações e permite simular ou registrar novas compras e vendas de itens.
    path('financeiro/', views.financeiro_view, name='financeiro'),
]