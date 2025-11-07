"""
URL configuration for config project.

O arquivo define as rotas principais do projeto Django.
Cada "path()" mapeia uma URL a um conjunto de views, seja de um app ou do painel de administração.
"""

from django.contrib import admin           # Importa o módulo de administração padrão do Django.
from django.urls import path, include      # Importa as funções path e include.

urlpatterns = [
    path('admin/', admin.site.urls),
    # 🔹 Define o caminho para o painel de administração.
    # Exemplo: http://localhost:8000/admin/
    # O Django já gera automaticamente as rotas e páginas dessa área.

    path('', include('apps.core.urls')),
    # 🔹 A rota vazia ('') redireciona para o arquivo apps/core/urls.py.
    # Isso significa que as rotas definidas em core.urls (como '/', '/sobre/') estarão acessíveis diretamente.
    # Exemplo: '/' → página inicial / 'sobre/' → página sobre.

    path('servicos/', include('apps.servicos.urls')),
    # 🔹 Essa rota define que todas as URLs que começarem com 'servicos/'
    # serão tratadas pelo arquivo apps/servicos/urls.py.
    # Exemplo: '/servicos/' → lista de combustíveis e serviços.

    path('accounts/', include('django.contrib.auth.urls'))
]
