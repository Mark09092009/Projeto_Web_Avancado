from django.shortcuts import render
from apps.gerenciamento.models import Servico


def lista_servicos(request):
    """Lista de Serviços cadastrados no sistema.

    Esta view consulta o modelo `Servico` (inclui serviços criados manualmente e
    os serviços espelho para combustíveis — sincronizados via `descricao`).
    """
    # garante que existem serviços básicos (seed) para o admin
    try:
        # Serviço 1: Troca de Óleo
        if not Servico.objects.filter(nome__iexact='Troca de Óleo').exists():
            Servico.objects.create(nome='Troca de Óleo', descricao='Troca de óleo padrão', preco_unitario=90.00)

        # Serviço 2: Balanceamento
        if not Servico.objects.filter(nome__iexact='Balanceamento').exists():
            Servico.objects.create(nome='Balanceamento', descricao='Balanceamento de rodas e pneus', preco_unitario=50.00)

        # Serviço 3: Alinhamento
        if not Servico.objects.filter(nome__iexact='Alinhamento').exists():
            Servico.objects.create(nome='Alinhamento', descricao='Alinhamento de direção do veículo', preco_unitario=80.00)
            
        # 4. Revisão Preventiva
        if not Servico.objects.filter(nome__iexact='Revisão Preventiva').exists():
            Servico.objects.create(nome='Revisão Preventiva', descricao='Verificação e manutenção de itens de segurança', preco_unitario=150.00)

        # 5. Troca de Pneus
        if not Servico.objects.filter(nome__iexact='Troca de Pneus').exists():
            Servico.objects.create(nome='Troca de Pneus', descricao='Remoção e instalação de pneus novos/usados', preco_unitario=40.00)
            
        # 6. Lavagem Completa
        if not Servico.objects.filter(nome__iexact='Lavagem Completa').exists():
            Servico.objects.create(nome='Lavagem Completa', descricao='Lavagem externa, interna e cera', preco_unitario=65.00)
            
        # Adicione mais serviços aqui, seguindo o mesmo padrão...

    except Exception:
        # não interrompe a view se houver problema na criação
        pass

    servicos_qs = Servico.objects.all().order_by('nome')
    return render(request, 'servicos/lista_servicos.html', {'servicos': servicos_qs})