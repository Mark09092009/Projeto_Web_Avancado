from django.shortcuts import render
from apps.gerenciamento.models import Servico


def lista_servicos(request):
    """Lista de Serviços cadastrados no sistema.

    Esta view consulta o modelo `Servico` (inclui serviços criados manualmente e
    os serviços espelho para combustíveis — sincronizados via `descricao`).
    """
    # garante que existem serviços básicos (seed) para o admin
    try:
        if not Servico.objects.filter(nome__iexact='Troca de Óleo').exists():
            Servico.objects.create(nome='Troca de Óleo', descricao='Troca de óleo padrão', preco_unitario=90.00)
    except Exception:
        # não interrompe a view se houver problema na criação
        pass

    servicos_qs = Servico.objects.all().order_by('nome')
    return render(request, 'servicos/lista_servicos.html', {'servicos': servicos_qs})
