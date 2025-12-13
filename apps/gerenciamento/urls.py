from django.urls import path
from . import views

urlpatterns = [
    path('estoque/', views.estoque_gasolina_view, name='estoque_gasolina'),
    path('estoque/visivel/', views.estoque_visivel_view, name='estoque_visivel'),
    path('estoque/adicionar/', views.adicionar_combustivel_view, name='adicionar_combustivel'),
    path('combustiveis/editar/', views.edit_combustiveis_view, name='edit_combustiveis'), 
    path('financeiro/', views.financeiro_view, name='financeiro'),
]