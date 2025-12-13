"""
URL configuration for config project.

Este arquivo define as rotas principais do projeto Django.
Cada função `path()` mapeia uma URL para um conjunto de views, seja de um app ou do painel de administração.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from apps.core.forms import EmailAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('apps.core.urls')),

    path('servicos/', include('apps.servicos.urls')),

    path('auth/login/', auth_views.LoginView.as_view(
        authentication_form=EmailAuthenticationForm,
        template_name='registration/login.html'
    ), name='login'),

    path('auth/', include('django.contrib.auth.urls')),

    path('gerenciamento/', include('apps.gerenciamento.urls')),
]