from django.urls import path   # Importa a função path, usada para criar rotas (URLs).
from . import views            # Importa o arquivo views.py do mesmo diretório (pasta 'core').

# Lista de rotas da aplicação 'core'
urlpatterns = [
    path('', views.home, name='home'),  
    # 🔹 Quando o usuário acessa a URL principal do site (ex: http://localhost:8000/),
    # o Django executa a função 'home' dentro de 'core/views.py'.
    # O parâmetro name='home' serve para referenciar essa rota no HTML usando {% url 'home' %}.

    path('sobre/', views.sobre, name='sobre'),
    # 🔹 Quando o usuário acessa a URL http://localhost:8000/sobre/,
    # o Django executa a função 'sobre' do arquivo 'core/views.py'.
    # O name='sobre' também permite gerar links facilmente no HTML.
]
