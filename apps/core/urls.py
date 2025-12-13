from django.urls import path 
from . import views 

# Lista de rotas (URLs) da aplicação 'core'
urlpatterns = [
    path('', views.home, name='home'),  
    path('sobre/', views.sobre, name='sobre'),
    path('register/', views.register, name='register'),
    path('contato/', views.contato, name='contato'),
    path('funcionarios/adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('funcionarios/register/', views.register_funcionario, name='register_funcionario'),
]