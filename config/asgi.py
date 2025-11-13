"""
ASGI config para o projeto `config`.

Este arquivo expõe o objeto WSGI/ASGI `application` que servidores
compatíveis (uvicorn, daphne, etc.) usam para servir a aplicação.

Traduzido/explicado em português para facilitar a leitura do projeto.
"""

import os

from django.core.asgi import get_asgi_application

# Define a variável de ambiente que aponta para as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Obtém o objeto ASGI que o servidor usará para lidar com requisições
application = get_asgi_application()
