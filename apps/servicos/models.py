"""
Módulo de modelos do aplicativo `servicos`.

Aqui normalmente conteríamos as definições de modelos específicos para o
aplicativo de serviços (ex.: serviços avulsos que o posto oferece). No
projeto atual as classes de domínio relacionadas a serviços e registros
financeiros estão implementadas no app `gerenciamento` (para manter o
domínio de estoque e financeiro centralizado). Mantemos este módulo
como placeholder com explicações para facilitar futuras adições.

Se for necessário, mover ou referenciar modelos entre apps deve ser feito
com imports relativos (por exemplo: `from apps.gerenciamento.models import Servico`).
"""

from django.db import models

# NOTE: neste projeto a implementação concreta de Servico/RegistroServico
# vive em `apps.gerenciamento.models`. Este arquivo está disponível como
# ponto de extensão para quando for decidido criar modelos específicos
# apenas para o app `servicos`.
