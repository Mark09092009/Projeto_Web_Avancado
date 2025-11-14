from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import RegistroCompra, RegistroVenda, EstoqueGasolina, Servico, RegistroServico
from .forms import MovimentacaoEstoqueForm, EstoqueGasolinaCreationForm, SimulacaoForm
from decimal import Decimal
from django.views.decorators.http import require_http_methods
from django.utils import timezone

@require_http_methods(["GET", "POST"])
def edit_combustiveis_view(request):
    """
    View responsável por listar todos os combustíveis e serviços e permitir
    a edição (em tempo real ou via submissão) do preço atual por litro/unidade.

    Métodos Suportados:
    - GET: Exibe a lista de itens e seus preços.
    - POST: Processa a submissão de um novo preço para um item.

    Lógica de POST (Atualização de Preço):
    1. Recebe 'pk' (formatado como 'C:1' ou 'S:2') e 'preco' (string).
    2. Converte a string 'preco' para Decimal para garantir precisão monetária.
    3. Analisa o prefixo ('C' ou 'S') para determinar se é Combustível ou Serviço.
    4. Atualiza o campo de preço (`preco_atual_litro` ou `preco_unitario`) no modelo.
    5. Adiciona uma mensagem de sucesso/erro e redireciona.
    """
    
    if request.method == 'POST':
        # Recebe os dados brutos da submissão (normalmente via JS em uma tabela)
        pk_raw = request.POST.get('pk')
        preco_str = request.POST.get('preco') 
        
        try:
            # 1. Converte o preço para Decimal IMEDIATAMENTE para evitar imprecisões de float.
            preco = Decimal(preco_str) 
            
            # 2. Faz o parsing do PK (chave primária) e do prefixo do tipo de item.
            # O pk_raw espera o formato 'C:1' (Combustível) ou 'S:2' (Serviço).
            if pk_raw and ':' in pk_raw:
                prefix, pk_str = pk_raw.split(':', 1)
            else:
                # Fallback: assume-se Combustível ('C') se o prefixo for omitido.
                prefix = 'C'
                pk_str = pk_raw

            pk = int(pk_str)

            # 3. Atualiza o preço com base no prefixo
            if prefix == 'C':
                item = EstoqueGasolina.objects.get(pk=pk)
                item.preco_atual_litro = preco 
                item.data_ultima_atualizacao = timezone.now() # Registra o timestamp da mudança de preço
                item.save()
                messages.success(request, f"Preço de {item.get_tipo_display()} atualizado para R$ {item.preco_atual_litro:.2f}")
            
            elif prefix == 'S':
                serv = Servico.objects.get(pk=pk)
                serv.preco_unitario = preco 
                serv.save()
                messages.success(request, f"Preço do serviço '{serv.nome}' atualizado para R$ {serv.preco_unitario:.2f}")

            return redirect('edit_combustiveis')
            
        except ValueError:
            # Captura erros de conversão (ex: preço não é um número válido)
            messages.error(request, "Erro: Preço inserido é inválido.")
        except EstoqueGasolina.DoesNotExist:
            messages.error(request, "Combustível não encontrado.")
        except Servico.DoesNotExist:
            messages.error(request, "Serviço não encontrado.")
        except Exception as e:
            # Captura erros inesperados durante a transação
            messages.error(request, f"Erro ao atualizar preço: {e}")

    # Lógica GET: Prepara os dados para exibição
    # Busca todos os combustíveis e serviços.
    estoques = EstoqueGasolina.objects.all().order_by('tipo')
    # Exclui serviços 'internos' (se houver, com base no prefixo na descrição)
    servicos = Servico.objects.exclude(descricao__startswith='origem:combustivel:').order_by('nome')
    
    context = {
        'estoques': estoques,
        'servicos': servicos,
        'titulo': 'Editar Combustíveis e Serviços'
    }
    return render(request, 'gerenciamento/edit_combustiveis.html', context)


def adicionar_combustivel_view(request):
    """
    View dedicada à criação inicial de um novo tipo de combustível no estoque.

    Fluxo de Trabalho:
    1. Identifica quais tipos de combustível (definidos no modelo) já foram cadastrados.
    2. Filtra as opções do formulário para mostrar APENAS os tipos que faltam.
    3. Se houver um tipo disponível, pré-carrega um preço sugerido.
    4. No POST, valida e salva o novo registro de EstoqueGasolina.
    """
    
    # 1. Obtém a lista dos códigos de tipos já existentes no banco
    tipos_existentes = list(EstoqueGasolina.objects.values_list('tipo', flat=True))
    
    # Redireciona se todos os tipos já estiverem cadastrados
    if len(tipos_existentes) >= len(EstoqueGasolina.TIPOS_COMBUSTIVEL):
        messages.info(request, "Todos os tipos de combustível já foram adicionados. Redirecionando para o controle de estoque.")
        return redirect('estoque_gasolina')

    # 2. Calcula as opções disponíveis (valor, label)
    tipos_disponiveis = [
        choice for choice in EstoqueGasolina.TIPOS_COMBUSTIVEL 
        if choice[0] not in tipos_existentes
    ]

    if request.method == 'POST':
        form = EstoqueGasolinaCreationForm(request.POST)
        
        # Garante que o campo 'tipo' do form utilize a lista filtrada de opções
        form.fields['tipo'].choices = tipos_disponiveis
        
        # Lógica para sugestão de preço (re-aplicada aqui por segurança)
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
        # Lógica GET: Inicializa o formulário e define as opções e sugestão
        form = EstoqueGasolinaCreationForm()
        form.fields['tipo'].choices = tipos_disponiveis
        
        # Define o preço inicial sugerido para o primeiro tipo na lista disponível
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
    """
    View para controle de estoque: visualização e movimentação de Combustíveis.

    Requisitos: Login do Usuário (@login_required).

    Fluxo de POST (Movimentação):
    1. Recebe o MovimentacaoEstoqueForm, validando quantidade e tipo.
    2. Utiliza `transaction.atomic()` e `select_for_update()` para garantir
       a integridade de dados em operações concorrentes.
    3. Calcula o `estoque_delta` (positivo para ENTRADA, negativo para SAIDA).
    4. Na SAIDA, verifica se o estoque é suficiente.
    5. Cria um RegistroCompra (ENTRADA) ou RegistroVenda (SAIDA).
    6. Atualiza a quantidade do EstoqueGasolina.
    """
    
    # 1. Verificação de Estoque Inicial
    if not EstoqueGasolina.objects.exists():
        messages.info(request, "O estoque está vazio. Por favor, adicione o estoque inicial dos seus combustíveis.")
        return redirect('adicionar_combustivel')

    if request.method == 'POST':
        form = MovimentacaoEstoqueForm(request.POST)
        
        if form.is_valid():
            combustivel_pk = form.cleaned_data['combustivel'].pk
            quantidade = form.cleaned_data['quantidade'] # Sempre positivo
            movimento = form.cleaned_data['movimento'] # 'ENTRADA' ou 'SAIDA'
            
            try:
                # Inicia a transação atômica para garantir ACID (atomicidade, consistência, isolamento, durabilidade)
                with transaction.atomic():
                    # select_for_update() bloqueia o registro de estoque no banco até o fim da transação
                    item_estoque = EstoqueGasolina.objects.select_for_update().get(pk=combustivel_pk)
                    
                    # Usa o preço atual de venda/compra registrado no modelo de estoque
                    preco_unitario = item_estoque.preco_atual_litro
                    
                    if movimento == 'SAIDA':
                        estoque_delta = quantidade * -1
                        # Validação crucial: Impede que o estoque fique negativo
                        if item_estoque.quantidade_litros + estoque_delta < 0:
                            messages.error(request, "ERRO: Estoque insuficiente para esta saída.")
                            return redirect('estoque_gasolina') 
                        
                        # Registra a transação de Venda
                        total = (Decimal(preco_unitario) * Decimal(quantidade))
                        RegistroVenda.objects.create(
                            combustivel=item_estoque,
                            quantidade_litros=quantidade,
                            preco_venda_litro=preco_unitario,
                            total_venda=total
                        )
                        msg_tipo = "Venda (Saída de Estoque)"
                        
                    else: # movimento == 'ENTRADA'
                        estoque_delta = quantidade

                        # Registra a transação de Compra
                        total = (Decimal(preco_unitario) * Decimal(quantidade))
                        RegistroCompra.objects.create(
                            combustivel=item_estoque,
                            quantidade_litros=quantidade,
                            preco_compra_litro=preco_unitario,
                            total_compra=total
                        )
                        msg_tipo = "Compra (Entrada de Estoque)"

                    # Atualiza o estoque no banco de dados e libera o lock
                    item_estoque.quantidade_litros += estoque_delta
                    item_estoque.save()

                    messages.success(request, f"{msg_tipo} registrada e Estoque de {item_estoque.get_tipo_display()} atualizado! ({'+' if estoque_delta > 0 else ''}{estoque_delta} L)")

            except EstoqueGasolina.DoesNotExist:
                messages.error(request, "Erro: Combustível não encontrado.")
            except Exception as e:
                messages.error(request, f"Erro inesperado ao atualizar estoque: {e}")
                
            return redirect('estoque_gasolina')
            
    else:
        # Lógica GET
        form = MovimentacaoEstoqueForm()
    
    # Busca e exibe o status atual de todos os estoques
    estoques = EstoqueGasolina.objects.all().order_by('tipo')
    
    context = {
        'estoques': estoques,
        'form': form,
        'titulo': 'Estoque de Combustíveis'
    }
    return render(request, 'gerenciamento/estoque_gasolina.html', context)


@login_required
def financeiro_view(request):
    """
    View de Gestão Financeira: exibe o histórico de transações e permite
    a simulação/registro de novas Compras/Vendas de combustíveis e serviços.

    Requisitos: Login do Usuário (@login_required).

    Fluxo Principal:
    1. Popula dinamicamente o campo 'item' do SimulacaoForm com Combustíveis (C:pk)
       e Serviços (S:pk).
    2. No POST, processa o item selecionado e o tipo de transação ('COMPRA'/'VENDA').
    3. Registra a transação (RegistroCompra/Venda/Servico) e atualiza o estoque (se for Combustível).
    4. Define 'is_entrada' para o template diferenciar Receita (True) de Custo (False).
    """
    
    # Busca os 10 últimos registros para exibição no histórico
    compras = RegistroCompra.objects.all()[:10]
    vendas = RegistroVenda.objects.all()[:10]
    registros_servicos = RegistroServico.objects.all()[:10]
    
    simulacao_resultado = None 
    
    # --- Preparação Dinâmica de Choices (Necessária para GET e POST) ---
    # Combustíveis (prefixo C:) e Serviços (prefixo S:) são combinados
    combustiveis = EstoqueGasolina.objects.all().order_by('tipo')
    # Filtra serviços para excluir aqueles usados para fins internos (se houver)
    servicos = Servico.objects.exclude(descricao__startswith='origem:combustivel:').order_by('nome')
    choices = []
    for c in combustiveis:
        # Formato: ('C:1', 'Combustível - Tipo (R$ Preço)')
        choices.append((f"C:{c.pk}", f"Combustível - {c.get_tipo_display()} (R$ {c.preco_atual_litro})"))
    for s in servicos:
        # Formato: ('S:2', 'Serviço - Nome (R$ Preço)')
        choices.append((f"S:{s.pk}", f"Serviço - {s.nome} (R$ {s.preco_unitario})"))
    # --- Fim da Preparação de Choices ---

    if request.method == 'POST':
        form = SimulacaoForm(request.POST)
        form.fields['item'].choices = choices # Atribui choices para a validação do POST

        if form.is_valid():
            item_raw = form.cleaned_data['item']
            quantidade = form.cleaned_data['quantidade']
            transacao = form.cleaned_data['transacao'] # 'COMPRA' ou 'VENDA'

            try:
                with transaction.atomic():
                    # Separa o prefixo (C/S) e o PK
                    prefix, pk_str = item_raw.split(':', 1)
                    pk = int(pk_str)
                    
                    is_entrada = False # Assume-se CUSTO (Saída de Caixa) inicialmente

                    if prefix == 'C':
                        # --- Fluxo de Combustível (Afeta Estoque) ---
                        item_estoque = EstoqueGasolina.objects.select_for_update().get(pk=pk)
                        preco_unitario = item_estoque.preco_atual_litro

                        if transacao == 'COMPRA':
                            # Compra: Entrada de Estoque, Saída de Caixa (Custo)
                            estoque_delta = quantidade
                            is_entrada = False 
                            total = (Decimal(preco_unitario) * Decimal(quantidade))
                            RegistroCompra.objects.create(
                                combustivel=item_estoque,
                                quantidade_litros=quantidade,
                                preco_compra_litro=preco_unitario,
                                total_compra=total
                            )
                            msg_tipo = "Compra de Combustível"

                        elif transacao == 'VENDA':
                            # Venda: Saída de Estoque, Entrada de Caixa (Receita)
                            estoque_delta = quantidade * -1
                            is_entrada = True 
                            
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
                            msg_tipo = "Venda de Combustível"

                        # Atualiza a quantidade no EstoqueGasolina
                        item_estoque.quantidade_litros += estoque_delta
                        item_estoque.save()

                        # Prepara dados para a mensagem de feedback
                        simulacao_resultado = {
                            'item_label': item_estoque.get_tipo_display(),
                            'quantidade': quantidade,
                            'preco_unitario': preco_unitario,
                            'total': total,
                            'tipo': transacao.lower(),
                            'is_entrada': is_entrada, 
                        }

                        messages.success(request, f"{msg_tipo} registrada e estoque atualizado!")

                    elif prefix == 'S':
                        # --- Fluxo de Serviço (Não Afeta Estoque) ---
                        servico = Servico.objects.get(pk=pk)
                        preco_unitario = servico.preco_unitario
                        total = (Decimal(preco_unitario) * Decimal(quantidade))
                        
                        # VENDA de Serviço é Receita (Entrada). COMPRA de Serviço é Custo (Saída).
                        is_entrada = transacao == 'VENDA'

                        RegistroServico.objects.create(
                            servico=servico,
                            tipo=transacao, # Armazena se foi 'COMPRA' ou 'VENDA' do serviço
                            quantidade=quantidade,
                            preco_unitario=preco_unitario,
                            total=total
                        )

                        # Prepara dados para a mensagem de feedback
                        simulacao_resultado = {
                            'item_label': servico.nome,
                            'quantidade': quantidade,
                            'preco_unitario': preco_unitario,
                            'total': total,
                            'tipo': transacao.lower(),
                            'is_entrada': is_entrada, 
                        }

                        messages.success(request, f"{transacao.title()} de serviço registrada!")

            except Exception as e:
                # Captura erros gerais de banco de dados, DoesNotExist, etc.
                messages.error(request, f"Erro na transação: {e}")

            return redirect('financeiro')
            
    else:
        # Lógica GET: Apenas inicializa o formulário com os choices dinâmicos
        form = SimulacaoForm()
        form.fields['item'].choices = choices # Atribui choices
        
    context = {
        'compras': compras,
        'vendas': vendas,
        'form': form,
        'simulacao_resultado': simulacao_resultado, # Usado para exibir o resultado da última transação
        'registros_servicos': registros_servicos,
        'titulo': 'Gestão Financeira'
    }
    return render(request, 'gerenciamento/financeiro.html', context)