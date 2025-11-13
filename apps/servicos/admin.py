"""
Admin module for o app `servicos`.

Este arquivo é o lugar onde se registrariam os modelos deste app para o
painel administrativo do Django. Atualmente o app `servicos` não declara
modelos próprios (eles residem em `apps.gerenciamento.models`), por isso
o registro explícito não é necessário aqui. Mantemos o arquivo para
clareza e futura extensão.

Caso adicione modelos no futuro, registre-os usando o padrão:

	from django.contrib import admin
	from .models import MeuModelo

	@admin.register(MeuModelo)
	class MeuModeloAdmin(admin.ModelAdmin):
		list_display = ('campo1', 'campo2')

"""

from django.contrib import admin

# Arquivo intencionalmente sem registros porque os modelos relevantes
# estão centralizados em `apps.gerenciamento.models`.
