"""
WSGI config para o projeto `config`.

Este arquivo disponibiliza a variável `application` que servidores WSGI
(por exemplo: gunicorn, uWSGI) usam para servir a aplicação em ambientes
de produção tradicionais.

Comentado em português para facilitar entendimento por desenvolvedores.
"""

import os

from django.core.wsgi import get_wsgi_application

# Define o settings module padrão caso a variável de ambiente não exista
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Cria/obtém a aplicação WSGI que o servidor web vai utilizar
application = get_wsgi_application()
