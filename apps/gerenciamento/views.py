from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import RegistroCompra, RegistroVenda, EstoqueGasolina, Servico, RegistroServico
from .forms import MovimentacaoEstoqueForm, EstoqueGasolinaCreationForm, SimulacaoForm
from django.db.models import Sum
from decimal import Decimal
from django.views.decorators.http import require_http_methods
from django.utils import timezone

@require_http_methods(["GET", "POST"])
def edit_combustiveis_view(request):
    """Aba para listar combustíveis e editar o preço atual por litro."""
    if request.method == 'POST':
        pk_raw = request.POST.get('pk')
        preco_str = request.POST.get('preco') # Recebe como string
        
        try:
            # 1. Converte o preço para Decimal IMEDIATAMENTE.
            preco = Decimal(preco_str) 
            
            # pk_raw may be prefixed like 'C:1' or 'S:2'
            if pk_raw and ':' in pk_raw:
                prefix, pk_str = pk_raw.split(':', 1)
            else:
                prefix = 'C'
                pk_str = pk_raw

            pk = int(pk_str)

            if prefix == 'C':
                item = EstoqueGasolina.objects.get(pk=pk)
                item.preco_atual_litro = preco # Usa o Decimal
                item.data_ultima_atualizacao = timezone.now() # Adicionado para atualizar a data no modelo
                item.save()
                messages.success(request, f"Preço de {item.get_tipo_display()} atualizado para R$ {item.preco_atual_litro:.2f}")
            elif prefix == 'S':
                serv = Servico.objects.get(pk=pk)
                serv.preco_unitario = preco # Usa o Decimal
                # serv.data_ultima_atualizacao = timezone.now() # O modelo Servico pode não ter esse campo
                serv.save()
                messages.success(request, f"Preço do serviço '{serv.nome}' atualizado para R$ {serv.preco_unitario:.2f}")

            return redirect('edit_combustiveis')
        except ValueError:
            messages.error(request, "Erro: Preço inserido é inválido.")
        except EstoqueGasolina.DoesNotExist:
            messages.error(request, "Combustível não encontrado.")
        except Servico.DoesNotExist:
            messages.error(request, "Serviço não encontrado.")
        except Exception as e:
            messages.error(request, f"Erro ao atualizar preço: {e}")

    estoques = EstoqueGasolina.objects.all().order_by('tipo')
    servicos = Servico.objects.exclude(descricao__startswith='origem:combustivel:').order_by('nome')
    context = {
        'estoques': estoques,
        'servicos': servicos,
        'titulo': 'Editar Combustíveis e Serviços'
    }
    return render(request, 'gerenciamento/edit_combustiveis.html', context)

def adicionar_combustivel_view(request):
    tipos_existentes = list(EstoqueGasolina.objects.values_list('tipo', flat=True))
    # Se já tiver todos os tipos cadastrados, redireciona para estoque
    if len(tipos_existentes) >= len(EstoqueGasolina.TIPOS_COMBUSTIVEL):
        messages.info(request, "Todos os tipos de combustível já foram adicionados. Redirecionando para o controle de estoque.")
        return redirect('estoque_gasolina')

    # calcula as opções disponíveis (valor, label) que ainda não existem no banco
    tipos_disponiveis = [
        choice for choice in EstoqueGasolina.TIPOS_COMBUSTIVEL 
        if choice[0] not in tipos_existentes
    ]

    if request.method == 'POST':
        form = EstoqueGasolinaCreationForm(request.POST)
        # garante que o campo 'tipo' do form só mostre as opções restantes
        form.fields['tipo'].choices = tipos_disponiveis
        # garante que o preço inicial sugerido corresponda à primeira opção disponível
        if tipos_disponiveis:
            first_tipo = tipos_disponiveis[0][0]
            suggested = EstoqueGasolinaCreationForm.PRECOS_BASE.get(first_tipo)
            if suggested is not None:
                form.fields['preco_atual_litro'].initial = suggested
        if form.is_valid():
            form.save()
            messages.success(request, f"O combustível {form.instance.get_tipo_display()} foi adicionado com sucesso ao estoque!")
            return redirect('estoque_gasolina')
    else:
        # passa a lista de choices antes de ajustar o preço sugerido
        form = EstoqueGasolinaCreationForm()
        form.fields['tipo'].choices = tipos_disponiveis
        if tipos_disponiveis:
            first_tipo = tipos_disponiveis[0][0]
            suggested = EstoqueGasolinaCreationForm.PRECOS_BASE.get(first_tipo)
            if suggested is not None:
                form.fields['preco_atual_litro'].initial = suggested
        
    context = {
        'form': form,
        'titulo': 'Adicionar Novo Combustível ao Estoque'
    }
    return render(request, 'gerenciamento/adicionar_combustivel.html', context)

@login_required
def estoque_gasolina_view(request):
    if not EstoqueGasolina.objects.exists():
        messages.info(request, "O estoque está vazio. Por favor, adicione o estoque inicial dos seus combustíveis.")
        return redirect('adicionar_combustivel')

    if request.method == 'POST':
        form = MovimentacaoEstoqueForm(request.POST)
        
        if form.is_valid():
            combustivel_pk = form.cleaned_data['combustivel'].pk
            quantidade = form.cleaned_data['quantidade']
            movimento = form.cleaned_data['movimento']
            
            try:
                with transaction.atomic():
                    item_estoque = EstoqueGasolina.objects.select_for_update().get(pk=combustivel_pk)
                    
                    # Usa o preço atual do estoque, não um preço fornecido pelo usuário
                    preco_unitario = item_estoque.preco_atual_litro
                    
                    if movimento == 'SAIDA':
                        estoque_delta = quantidade * -1
                        if item_estoque.quantidade_litros + estoque_delta < 0:
                            messages.error(request, "ERRO: Estoque insuficiente para esta saída.")
                            return redirect('estoque_gasolina') 
                    else:
                        estoque_delta = quantidade

                    item_estoque.quantidade_litros += estoque_delta
                    item_estoque.save()

                    if movimento == 'ENTRADA':
                        total = (Decimal(preco_unitario) * Decimal(quantidade))
                        RegistroCompra.objects.create(
                            combustivel=item_estoque,
                            quantidade_litros=quantidade,
                            preco_compra_litro=preco_unitario,
                            total_compra=total
                        )
                        msg_tipo = "Compra (Entrada de Estoque)"
                    
                    elif movimento == 'SAIDA':
                        total = (Decimal(preco_unitario) * Decimal(quantidade))
                        RegistroVenda.objects.create(
                            combustivel=item_estoque,
                            quantidade_litros=quantidade,
                            preco_venda_litro=preco_unitario,
                            total_venda=total
                        )
                        msg_tipo = "Venda (Saída de Estoque)"

                    messages.success(request, f"{msg_tipo} registrada e Estoque de {item_estoque.get_tipo_display()} atualizado! ({'+' if estoque_delta > 0 else ''}{estoque_delta} L)")

            except EstoqueGasolina.DoesNotExist:
                messages.error(request, "Erro: Combustível não encontrado.")
            except Exception as e:
                messages.error(request, f"Erro inesperado ao atualizar estoque: {e}")
                
            return redirect('estoque_gasolina')
            
    else:
        form = MovimentacaoEstoqueForm()
    
    estoques = EstoqueGasolina.objects.all().order_by('tipo')
    
    context = {
        'estoques': estoques,
        'form': form,
        'titulo': 'Estoque de Combustíveis'
    }
    return render(request, 'gerenciamento/estoque_gasolina.html', context)

@login_required
def financeiro_view(request):
    compras = RegistroCompra.objects.all()[:10]
    vendas = RegistroVenda.objects.all()[:10]
    registros_servicos = RegistroServico.objects.all()[:10]
    
    simulacao_resultado = None
    
    if request.method == 'POST':
        form = SimulacaoForm(request.POST)
        # build dynamic choices (prefix with C: for combustivel, S: for servico)
        combustiveis = EstoqueGasolina.objects.all().order_by('tipo')
        # only non-fuel services
        servicos = Servico.objects.exclude(descricao__startswith='origem:combustivel:').order_by('nome')
        choices = []
        for c in combustiveis:
            choices.append((f"C:{c.pk}", f"Combustível - {c.get_tipo_display()} (R$ {c.preco_atual_litro})"))
        for s in servicos:
            choices.append((f"S:{s.pk}", f"Serviço - {s.nome} (R$ {s.preco_unitario})"))
        form.fields['item'].choices = choices # set choices again in case of validation error path

        if form.is_valid():
            item_raw = form.cleaned_data['item']
            quantidade = form.cleaned_data['quantidade']
            transacao = form.cleaned_data['transacao']

            try:
                with transaction.atomic():
                    prefix, pk_str = item_raw.split(':', 1)
                    pk = int(pk_str)
                    
                    # Assume False inicialmente para evitar erro, se for VENDA/entrada, será True
                    is_entrada = False

                    if prefix == 'C':
                        # combustível flow (affects estoque)
                        item_estoque = EstoqueGasolina.objects.select_for_update().get(pk=pk)
                        preco_unitario = item_estoque.preco_atual_litro

                        if transacao == 'COMPRA':
                            estoque_delta = quantidade
                            is_entrada = False # Compra = Saída de Caixa
                            total = (Decimal(preco_unitario) * Decimal(quantidade))
                            RegistroCompra.objects.create(
                                combustivel=item_estoque,
                                quantidade_litros=quantidade,
                                preco_compra_litro=preco_unitario,
                                total_compra=total
                            )
                            msg_tipo = "Compra"

                        elif transacao == 'VENDA':
                            estoque_delta = quantidade * -1
                            is_entrada = True # Venda = Entrada de Caixa
                            if item_estoque.quantidade_litros + estoque_delta < 0:
                                messages.error(request, "ERRO: Estoque insuficiente para registrar esta venda.")
                                return redirect('financeiro')

                            total = (Decimal(preco_unitario) * Decimal(quantidade))
                            RegistroVenda.objects.create(
                                combustivel=item_estoque,
                                quantidade_litros=quantidade,
                                preco_venda_litro=preco_unitario,
                                total_venda=total
                            )
                            msg_tipo = "Venda"

                        item_estoque.quantidade_litros += estoque_delta
                        item_estoque.save()

                        simulacao_resultado = {
                            'item_label': item_estoque.get_tipo_display(),
                            'quantidade': quantidade,
                            'preco_unitario': preco_unitario,
                            'total': total,
                            'tipo': transacao.lower(),
                            'is_entrada': is_entrada, # <<<<<< ADIÇÃO CHAVE
                        }

                        messages.success(request, f"{msg_tipo} registrada e estoque atualizado!")

                    elif prefix == 'S':
                        # service flow (does not change fuel stock)
                        servico = Servico.objects.get(pk=pk)
                        preco_unitario = servico.preco_unitario
                        total = (Decimal(preco_unitario) * Decimal(quantidade))
                        
                        # Determina se é entrada ou saída para a simulação/template
                        is_entrada = transacao == 'VENDA'

                        RegistroServico.objects.create(
                            servico=servico,
                            tipo=transacao,
                            quantidade=quantidade,
                            preco_unitario=preco_unitario,
                            total=total
                        )

                        simulacao_resultado = {
                            'item_label': servico.nome,
                            'quantidade': quantidade,
                            'preco_unitario': preco_unitario,
                            'total': total,
                            'tipo': transacao.lower(),
                            'is_entrada': is_entrada, # <<<<<< ADIÇÃO CHAVE
                        }

                        messages.success(request, f"{transacao.title()} de serviço registrada!")

            except Exception as e:
                messages.error(request, f"Erro na transação: {e}")

            return redirect('financeiro')
        
    else:
        form = SimulacaoForm()
        # populate choices combining combustíveis and serviços
        combustiveis = EstoqueGasolina.objects.all().order_by('tipo')
        servicos = Servico.objects.exclude(descricao__startswith='origem:combustivel:').order_by('nome')
        choices = []
        for c in combustiveis:
            choices.append((f"C:{c.pk}", f"Combustível - {c.get_tipo_display()} (R$ {c.preco_atual_litro})"))
        for s in servicos:
            choices.append((f"S:{s.pk}", f"Serviço - {s.nome} (R$ {s.preco_unitario})"))
        form.fields['item'].choices = choices
        
    context = {
        'compras': compras,
        'vendas': vendas,
        'form': form,
        'simulacao_resultado': simulacao_resultado,
        'registros_servicos': registros_servicos,
        'titulo': 'Gestão Financeira'
    }
    return render(request, 'gerenciamento/financeiro.html', context)