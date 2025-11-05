from django.contrib import admin
from django.urls import path, include

from apps.autenticacao.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', include('apps.clientes.urls')),
    path('produtos/', include('apps.produtos.urls')),
    path('vendas/', include('apps.vendas.urls')),
    path('relatorios/', include('apps.relatorios.urls')),
    path('auth/', include('apps.autenticacao.urls')),
    path('', login_view, name='login')
]
