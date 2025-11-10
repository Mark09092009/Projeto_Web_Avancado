from django.urls import path   # Importa a função 'path' do Django, usada para definir rotas (URLs) da aplicação.
from . import views            # Importa o módulo 'views' da mesma pasta onde este arquivo está localizado.

# Define a lista de rotas (URLs) da aplicação 'servicos'.
urlpatterns = [
    # Define a rota base da aplicação 'servicos'.
    # Quando o usuário acessa a URL base (exemplo: http://localhost:8000/servicos/),
    # o Django chama a função 'lista_servicos' que está definida no arquivo 'views.py' da aplicação 'servicos'.
    path('', views.lista_servicos, name='lista_servicos'),

    # O parâmetro 'name' é usado para nomear a rota. Isso permite criar links dinâmicos no HTML
    # usando a tag template do Django: {% url 'lista_servicos' %}.
]
