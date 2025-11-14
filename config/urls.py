"""
URL configuration for config project.

Este arquivo define as rotas principais do projeto Django.
Cada função `path()` mapeia uma URL para um conjunto de views, seja de um app ou do painel de administração.
"""

from django.contrib import admin  # Importa o módulo de administração padrão do Django.
from django.urls import path, include  # Importa as funções `path` e `include` para definir rotas.
from django.contrib.auth import views as auth_views  # Importa as views de autenticação padrão do Django.

# IMPORTANTE: Importa o formulário de autenticação personalizado que criamos.
from apps.core.forms import EmailAuthenticationForm

# Lista de padrões de URL do projeto.
urlpatterns = [
    # Rota para o painel de administração do Django.
    path('admin/', admin.site.urls),

    # Rota principal do projeto, que inclui as URLs do app `core`.
    path('', include('apps.core.urls')),

    # Rota para o app `servicos`, que gerencia as URLs relacionadas a serviços.
    path('servicos/', include('apps.servicos.urls')),

    # Configuração personalizada para a rota de login.
    # Aqui, usamos a view padrão de login do Django (`LoginView`) com um formulário de autenticação personalizado
    # (`EmailAuthenticationForm`) e um template específico (`registration/login.html`).
    path('auth/login/', auth_views.LoginView.as_view(
        authentication_form=EmailAuthenticationForm,  # Formulário de login personalizado.
        template_name='registration/login.html'  # Template usado para a página de login.
    ), name='login'),

    # Inclui as rotas padrão de autenticação do Django (logout, password reset, etc.).
    # Essas rotas são fornecidas pelo módulo `django.contrib.auth.urls`.
    path('auth/', include('django.contrib.auth.urls')),

    # Inclui as rotas para os elementos do gerenciamento.
    path('gerenciamento/', include('apps.gerenciamento.urls')),
]