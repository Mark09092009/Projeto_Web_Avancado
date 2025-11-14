from django.shortcuts import render
from apps.gerenciamento.models import Servico


def lista_servicos(request):
    try:
        if not Servico.objects.filter(nome__iexact='Troca de Óleo').exists():
            Servico.objects.create(nome='Troca de Óleo', descricao='Troca de óleo padrão', preco_unitario=90.00)

        if not Servico.objects.filter(nome__iexact='Balanceamento').exists():
            Servico.objects.create(nome='Balanceamento', descricao='Balanceamento de rodas e pneus', preco_unitario=50.00)

        if not Servico.objects.filter(nome__iexact='Alinhamento').exists():
            Servico.objects.create(nome='Alinhamento', descricao='Alinhamento de direção do veículo', preco_unitario=80.00)

        if not Servico.objects.filter(nome__iexact='Revisão Preventiva').exists():
            Servico.objects.create(nome='Revisão Preventiva', descricao='Verificação e manutenção de itens de segurança', preco_unitario=150.00)

        if not Servico.objects.filter(nome__iexact='Troca de Pneus').exists():
            Servico.objects.create(nome='Troca de Pneus', descricao='Remoção e instalação de pneus novos/usados', preco_unitario=40.00)

        if not Servico.objects.filter(nome__iexact='Lavagem Completa').exists():
            Servico.objects.create(nome='Lavagem Completa', descricao='Lavagem externa, interna e cera', preco_unitario=65.00)

    except Exception:
        pass

    servicos_qs = Servico.objects.all().order_by('nome')
    return render(request, 'servicos/lista_servicos.html', {'servicos': servicos_qs})
