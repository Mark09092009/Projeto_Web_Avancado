from django.contrib import admin
from .models import EstoqueGasolina, Servico, RegistroServico


@admin.register(EstoqueGasolina)
class EstoqueGasolinaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'quantidade_litros', 'data_ultima_atualizacao')
    list_filter = ('tipo',)
    search_fields = ('tipo',)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_unitario', 'criado_em')
    search_fields = ('nome',)


@admin.register(RegistroServico)
class RegistroServicoAdmin(admin.ModelAdmin):
    list_display = ('servico', 'tipo', 'quantidade', 'preco_unitario', 'total', 'data')
    list_filter = ('tipo',)
    search_fields = ('servico__nome',)
