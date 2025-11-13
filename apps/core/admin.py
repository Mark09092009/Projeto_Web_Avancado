"""
Módulo de configuração do admin para o aplicativo `core`.

Utilize este arquivo para customizar como os modelos do app `core`
aparecerão no painel administrativo do Django. Por enquanto não há
modelos para registrar, portanto o arquivo atua como um ponto de
extensão futuro.

Exemplo de uso:

	from django.contrib import admin
	from .models import MeuModelo

	@admin.register(MeuModelo)
	class MeuModeloAdmin(admin.ModelAdmin):
		list_display = ('campo1', 'campo2')

"""

from django.contrib import admin

# Arquivo mantido para registrar modelos do app `core` quando necessário.
