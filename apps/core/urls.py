from django.urls import path   # Importa a função 'path', que é usada para definir as rotas (URLs) da aplicação.
from . import views            # Importa o módulo 'views' do mesmo diretório, onde estão as funções que tratam as requisições.

# Lista de rotas (URLs) da aplicação 'core'
urlpatterns = [
    path('', views.home, name='home'),  
    # Define a rota principal (URL raiz, ex: http://localhost:8000/).
    # Quando o usuário acessa essa URL, a função 'home' do arquivo 'views.py' será executada.
    # O parâmetro 'name="home"' permite referenciar essa rota no HTML usando a tag {% url 'home' %}.

    path('sobre/', views.sobre, name='sobre'),
    # Define a rota para a URL http://localhost:8000/sobre/.
    # Quando o usuário acessa essa URL, a função 'sobre' do arquivo 'views.py' será executada.
    # O parâmetro 'name="sobre"' também permite criar links para essa rota no HTML.

    path('register/', views.register, name='register'),
    # Define a rota para a URL http://localhost:8000/register/.
    # Quando o usuário acessa essa URL, a função 'register' do arquivo 'views.py' será executada.
    # O parâmetro 'name="register"' facilita a criação de links para essa rota no HTML.

    path('contato/', views.contato, name='contato'),
]
