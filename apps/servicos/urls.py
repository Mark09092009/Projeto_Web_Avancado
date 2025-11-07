from django.urls import path   # Importa a função path para criar rotas (URLs).
from . import views            # Importa o arquivo views.py da pasta 'servicos'.

# Lista de rotas da aplicação 'servicos'
urlpatterns = [
    path('', views.lista_servicos, name='lista_servicos'),
    # 🔹 Quando o usuário acessa a URL base da aplicação 'servicos' (ex: http://localhost:8000/servicos/),
    # o Django executa a função 'lista_servicos' definida em 'servicos/views.py'.
    # 🔹 O parâmetro name='lista_servicos' serve para criar links dinâmicos no HTML usando {% url 'lista_servicos' %}.
]
