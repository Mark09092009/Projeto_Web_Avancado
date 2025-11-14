"""

Este arquivo contém comentários explicativos detalhados para cada
formulário, seus campos, validações e widgets. Também informei a
página (ou tela) do sistema onde cada formulário costuma ser usado.

Páginas correspondentes:
- MovimentacaoEstoqueForm  -> Página: "Movimentação de Estoque" (Interface para adicionar/retirar combustível).
- EstoqueGasolinaCreationForm -> Página: "Cadastro de Estoque" / "Configuração Inicial de Estoque" (Formulário administrador para criar tipos/estoque inicial).
- SimulacaoForm -> Página: "Simulação Financeira" (Tela que permite simular compras/vendas sem gravar no banco).

Observação: os nomes das páginas podem variar conforme a organização do projeto. Adapte os títulos às rotas/URLs que você usa no projeto (ex.: `gerenciamento/movimentacao/`, `gerenciamento/estoque/adicionar/`, `gerenciamento/simulacao/`).
"""

from django import forms
from .models import EstoqueGasolina


class MovimentacaoEstoqueForm(forms.Form):
    """
    Formulário simples (não ModelForm) para movimentações de estoque.

    Página: "Movimentação de Estoque" — usada quando o usuário precisa
    registrar entradas (reposição) ou saídas (venda/consumo) de combustível.

    Observações de uso:
    - O preço unitário não é permitido aqui — deve ser obtido na View a
      partir do modelo `EstoqueGasolina.preco_atual_litro` para manter
      consistência de preços.
    - A `quantidade` é obrigatoriamente positiva (min_value=0.01). Para
      saídas, a View deve subtrair essa quantidade do estoque.
    - `movimento` diferencia ENTRE/SAÍDA para facilitar a lógica na View.
    """

    # Tipos de movimentação apresentados ao usuário (rótulos amigáveis)
    TIPO_MOVIMENTACAO = [
        ('ENTRADA', 'Entrada (+ Adicionar)'),
        ('SAIDA', 'Saída (- Remover)'),
    ]

    # Campo de seleção do tipo de combustível.
    # - ModelChoiceField: popula opções diretamente do modelo EstoqueGasolina.
    # - queryset ordenado por 'tipo' para apresentar uma lista previsível.
    # - empty_label fornece um texto quando nada foi selecionado.
    # - widget com classe Bootstrap para manter estilo consistente com o site.
    combustivel = forms.ModelChoiceField(
        queryset=EstoqueGasolina.objects.all().order_by('tipo'),
        label="Combustível",
        empty_label="Selecione o Combustível",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Quantidade em litros. Sempre positivo para simplificar tratamento.
    # - max_digits/decimal_places devem suportar quantidades e precisão
    #   esperadas (ex.: tanques grandes).
    # - placeholder ajuda o usuário a entender o formato esperado.
    quantidade = forms.DecimalField(
        label="Quantidade (Litros)",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 10.00'})
    )

    # Tipo de movimento: escolha entre ENTRADA ou SAIDA.
    # - Na View, usar este campo para decidir somar/subtrair do estoque.
    movimento = forms.ChoiceField(
        choices=TIPO_MOVIMENTACAO,
        label="Tipo de Movimento",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Observação livre, opcional — útil para auditoria e histórico.
    observacao = forms.CharField(
        label="Observação (Opcional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Recebimento de Cargas'})
    )


class EstoqueGasolinaCreationForm(forms.ModelForm):
    """
    ModelForm para a criação inicial de um registro de estoque de
    combustível (tipicamente usada por admin ou usuário autorizado).

    Página: "Cadastro de Estoque" / "Configuração Inicial de Estoque"
    — tela onde se adiciona um novo tipo de combustível ao sistema com
    quantidade inicial e preço.

    Recursos e comportamento:
    - Sugere preços iniciais baseados em PRECOS_BASE ao renderizar o form
      em GET (melhora a usabilidade evitando que o usuário precise lembrar valores).
    - Evita duplicação de tipos: clean_tipo() valida unicidade do campo `tipo`.
    - Widgets configurados com classes Bootstrap para aparência consistente.
    """

    # Dicionário com preços base sugeridos (por tipo de combustível).
    # Esses valores servem apenas como sugestão inicial e podem ser
    # ajustados pelo usuário antes de salvar.
    PRECOS_BASE = {
        'GAS_COMUM': 5.50,
        'GAS_ADITIVADA': 6.20,
        'DIESEL_COMUM': 6.00,
        'DIESEL_S10': 6.50,
        'ETANOL': 4.50,
    }

    class Meta:
        model = EstoqueGasolina
        # Campos expostos ao criar um novo tipo de combustível
        fields = ['tipo', 'quantidade_litros', 'preco_atual_litro']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_litros': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade inicial em Litros'}),
            'preco_atual_litro': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço por Litro (R$)'}),
        }

    def clean_tipo(self):
        """
        Validação customizada para garantir que um mesmo tipo de
        combustível não seja cadastrado duas vezes.

        Implementação: consulta o banco para verificar existência de
        `tipo`. Levanta ValidationError se já existir.
        """
        tipo = self.cleaned_data.get('tipo')
        if EstoqueGasolina.objects.filter(tipo=tipo).exists():
            raise forms.ValidationError("Este tipo de combustível já existe. Use o formulário de Movimentação para atualizá-lo.")
        return tipo

    def __init__(self, *args, **kwargs):
        """
        Personaliza a inicialização do formulário:
        - Ao criar (instância nova): tenta pré-preencher `preco_atual_litro`
          com um valor sugerido de PRECOS_BASE com base na primeira escolha
          do campo `tipo` (ou com um fallback).
        - Ao editar (instância existente com pk): mantém o valor da instância.
        - Adiciona help_text ao campo de preço para avisar que é apenas
          uma sugestão.
        """
        super().__init__(*args, **kwargs)

        # Se estiver editando uma instância existente, preserva o valor
        if self.instance and self.instance.pk:
            self.fields['preco_atual_litro'].initial = self.instance.preco_atual_litro
        else:
            # tentativa de inferir a primeira opção do campo `tipo`
            tipo_field = self.fields.get('tipo')
            first_choice = None
            if tipo_field is not None and hasattr(tipo_field, 'choices'):
                choices = list(tipo_field.choices)
                if choices:
                    # choices geralmente são tuplas (valor, rótulo)
                    first_choice = choices[0][0]

            # se a primeira opção existir e tivermos preço base correspondente,
            # usamos esse preço como sugestão inicial
            if first_choice and first_choice in self.PRECOS_BASE:
                self.fields['preco_atual_litro'].initial = self.PRECOS_BASE[first_choice]
            else:
                # fallback: pega qualquer preço do dicionário ou 0.00
                any_price = next(iter(self.PRECOS_BASE.values())) if self.PRECOS_BASE else 0.00
                self.fields['preco_atual_litro'].initial = any_price

        # ajuda visual ao usuário informando que o preço é sugerido
        self.fields['preco_atual_litro'].help_text = "Preço sugerido já preenchido. Ajuste conforme necessário."


class SimulacaoForm(forms.Form):
    """
    Formulário para simulações financeiras — NÃO grava nada no banco.

    Página: "Simulação Financeira" — usada para calcular valores de
    compra/venda estimados antes de efetivar uma movimentação.

    Observações de uso:
    - O campo `item` é preenchido dinamicamente pela View (choices com
      prefixos como 'C:pk' para Combustível e 'S:pk' para Serviço).
    - Preço não é exposto ao usuário aqui: a View deverá buscar o preço
      unitário correspondente ao item selecionado no modelo (ex.: EstoqueGasolina.preco_atual_litro ou Servico.preco_unitario).
    """

    # choices=[] deixado vazio intencionalmente; a View deve setar choices
    # antes de renderizar o formulário (ex.: form.fields['item'].choices = ...)
    item = forms.ChoiceField(
        choices=[],
        label="Item (Combustível ou Serviço)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Tipo de transação que está sendo simulada: COMPRA (entrada) ou VENDA (saída)
    TIPO_TRANSACAO = [
        ('COMPRA', 'Simular Compra (Entrada)'),
        ('VENDA', 'Simular Venda (Saída)'),
    ]
    transacao = forms.ChoiceField(
        choices=TIPO_TRANSACAO,
        label="Tipo de Transação",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Quantidade a simular (por exemplo, litros ou unidades de serviço)
    quantidade = forms.DecimalField(
        label="Quantidade",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'})
    )

    # Nota: não há campo para preço — a View responsável pela simulação
    # deve buscar o preço fixo do modelo correspondente ao item selecionado.
