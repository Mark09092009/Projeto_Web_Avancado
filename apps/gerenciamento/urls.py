"""
URLs do aplicativo `gerenciamento`.

Define as rotas para gestão de estoque, movimentações e financeiro.
Cada rota referencia uma view no módulo `views` deste app.
"""

from django.urls import path
from . import views

# Lista de rotas específicas do app 'gerenciamento'
urlpatterns = [
    path('estoque/', views.estoque_gasolina_view, name='estoque_gasolina'),
    path('estoque/adicionar/', views.adicionar_combustivel_view, name='adicionar_combustivel'),
    # 'edit_combustiveis' é a rota para a view que renderiza o Template 1
    path('combustiveis/editar/', views.edit_combustiveis_view, name='edit_combustiveis'), 
    path('financeiro/', views.financeiro_view, name='financeiro'),
]