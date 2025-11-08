"""
URL configuration for config project.

O arquivo define as rotas principais do projeto Django.
Cada "path()" mapeia uma URL a um conjunto de views, seja de um app ou do painel de administração.
"""

from django.contrib import admin # Importa o módulo de administração padrão do Django.
from django.urls import path, include # Importa as funções path e include.
from django.contrib.auth import views as auth_views # Importa as views de autenticação do Django

# 🚨 IMPORTANTE: Importe o novo formulário de login que criamos
from apps.core.forms import EmailAuthenticationForm 

urlpatterns = [
    path('admin/', admin.site.urls),
    # 🔹 Define o caminho para o painel de administração.

    path('', include('apps.core.urls')),
    # 🔹 Rota principal.

    path('servicos/', include('apps.servicos.urls')),
    # 🔹 Rota para serviços.

    # 🚨 ALTERAÇÃO: Configura a rota 'login' explicitamente usando o formulário personalizado.
    # O restante das rotas de autenticação (logout, password reset) serão incluídas
    # a partir de 'django.contrib.auth.urls' no final.
    path('auth/login/', auth_views.LoginView.as_view(
        authentication_form=EmailAuthenticationForm, 
        template_name='registration/login.html' # Ajuste este template se for diferente
    ), name='login'),
    
    # 🔹 Inclui o restante das URLs de autenticação (logout, password reset, etc.)
    path('auth/', include('django.contrib.auth.urls')),
]