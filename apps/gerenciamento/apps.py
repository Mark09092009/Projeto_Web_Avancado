"""
Configuração do app `gerenciamento`.

Define a classe AppConfig que registra o app junto ao Django.
Usado pelo framework para detectar configurações específicas do app.
"""

from django.apps import AppConfig


class GerenciamentoConfig(AppConfig):
    # Tipo padrão para chaves primárias automáticas
    default_auto_field = 'django.db.models.BigAutoField'
    # Nome usado pelo Django para referenciar o pacote do app
    name = 'apps.gerenciamento'
