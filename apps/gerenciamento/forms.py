"""
Formulários do app `gerenciamento`.

Contêm formulários para movimentação de estoque, criação inicial de
estoque e simulações financeiras. Os formulários encapsulam validações
e configurações de widgets (classes CSS para Bootstrap).
"""

from django import forms
from .models import EstoqueGasolina

class MovimentacaoEstoqueForm(forms.Form):
    # Tipos de Movimentação para o usuário
    TIPO_MOVIMENTACAO = [
        ('ENTRADA', 'Entrada (+ Adicionar)'),
        ('SAIDA', 'Saída (- Remover)'),
    ]

    # Campo de seleção do tipo de combustível
    combustivel = forms.ModelChoiceField(
        queryset=EstoqueGasolina.objects.all().order_by('tipo'),
        label="Combustível",
        empty_label="Selecione o Combustível",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Campo para a quantidade (deve ser sempre um valor positivo para facilitar o cálculo na View)
    quantidade = forms.DecimalField(
        label="Quantidade (Litros)",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1000.00'})
    )

    # Campo para selecionar se é entrada ou saída
    movimento = forms.ChoiceField(
        choices=TIPO_MOVIMENTACAO,
        label="Tipo de Movimento",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Nota: o preço unitário é obtido automaticamente do estoque (preco_atual_litro)
    # não é permitido ao usuário alterar o preço durante uma movimentação
    
    # Adicionar uma observação é opcional, mas útil para auditoria
    observacao = forms.CharField(
        label="Observação (Opcional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Recebimento de Cargas'})
    )

# - Classe para adicionar as opções de gasolina diretamente do site
class EstoqueGasolinaCreationForm(forms.ModelForm):
    # Preços base realistas por tipo de combustível (em Reais por litro)
    PRECOS_BASE = {
        'GAS_COMUM': 5.50,
        'GAS_ADITIVADA': 6.20,
        'DIESEL_COMUM': 6.00,
        'DIESEL_S10': 6.50,
        'ETANOL': 4.50,
    }

    class Meta:
        model = EstoqueGasolina
        # Campos para a criação inicial: tipo, estoque inicial e preço inicial
        fields = ['tipo', 'quantidade_litros', 'preco_atual_litro'] 
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_litros': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade inicial em Litros'}),
            'preco_atual_litro': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço por Litro (R$)'})
        }

    # Validação para garantir que o tipo de combustível não foi adicionado antes
    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if EstoqueGasolina.objects.filter(tipo=tipo).exists():
            raise forms.ValidationError("Este tipo de combustível já existe. Use o formulário de Movimentação para atualizá-lo.")
        return tipo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preenche um preço inicial sugerido quando o form é exibido em GET
        # Se o form estiver vinculado a uma instância (edição), usa o valor da instância
        if self.instance and self.instance.pk:
            # edição — mantém o valor atual do objeto
            self.fields['preco_atual_litro'].initial = self.instance.preco_atual_litro
        else:
            # criação — tenta usar o primeiro tipo disponível ou a primeira chave do PRECOS_BASE
            # obter primeira opção do campo 'tipo' (se houver)
            tipo_field = self.fields.get('tipo')
            first_choice = None
            if tipo_field is not None and hasattr(tipo_field, 'choices'):
                choices = list(tipo_field.choices)
                if choices:
                    # choices entries may be tuples like ('GAS_COMUM', 'Gasolina Comum')
                    first_choice = choices[0][0]

            if first_choice and first_choice in self.PRECOS_BASE:
                self.fields['preco_atual_litro'].initial = self.PRECOS_BASE[first_choice]
            else:
                # fallback: pick any price from PRECOS_BASE
                any_price = next(iter(self.PRECOS_BASE.values())) if self.PRECOS_BASE else 0.00
                self.fields['preco_atual_litro'].initial = any_price
        # Adiciona help_text para mostrar preço sugerido
        self.fields['preco_atual_litro'].help_text = "Preço sugerido já preenchido. Ajuste conforme necessário."
    
class SimulacaoForm(forms.Form):
    # Item é uma escolha dinâmica que pode representar um combustível (prefixo C:pk)
    # ou um serviço (prefixo S:pk). O view montará choices apropriadas.
    item = forms.ChoiceField(
        choices=[],
        label="Item (Combustível ou Serviço)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Simula se é compra ou venda
    TIPO_TRANSACAO = [
        ('COMPRA', 'Simular Compra (Entrada)'),
        ('VENDA', 'Simular Venda (Saída)'),
    ]
    transacao = forms.ChoiceField(
        choices=TIPO_TRANSACAO,
        label="Tipo de Transação",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    quantidade = forms.DecimalField(
        label="Quantidade",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'})
    )

    # Não permitimos alterar o preço na simulação: o preço será obtido a partir
    # do modelo (EstoqueGasolina.preco_atual_litro ou Servico.preco_unitario).
