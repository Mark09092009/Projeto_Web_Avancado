#!/usr/bin/env python
"""
Entrypoint de linha de comando do Django para tarefas administrativas.

Este script é o wrapper padrão gerado pelo Django e permite executar
comandos como `runserver`, `migrate`, `createsuperuser`, etc. Em geral não
é necessário modificá-lo, mas é útil ter documentação rápida sobre seu uso.
"""

import os
import sys


def main():
    """Executa tarefas administrativas usando a API de gerenciamento do Django.

    Define a variável de ambiente `DJANGO_SETTINGS_MODULE` caso não esteja
    definida e delega a execução para `django.core.management.execute_from_command_line`.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
