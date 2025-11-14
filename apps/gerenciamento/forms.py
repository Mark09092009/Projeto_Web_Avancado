from django import forms
from .models import EstoqueGasolina
from decimal import Decimal


class MovimentacaoEstoqueForm(forms.Form):
    TIPO_MOVIMENTACAO = [
        ('ENTRADA', 'Entrada (+ Adicionar)'),
        ('SAIDA', 'Saída (- Remover)'),
    ]

    combustivel = forms.ModelChoiceField(
        queryset=EstoqueGasolina.objects.all().order_by('tipo'),
        label="Combustível",
        empty_label="Selecione o Combustível",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    quantidade = forms.DecimalField(
        label="Quantidade (Litros)",
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 10.00'})
    )

    movimento = forms.ChoiceField(
        choices=TIPO_MOVIMENTACAO,
        label="Tipo de Movimento",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    observacao = forms.CharField(
        label="Observação (Opcional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Recebimento de Cargas'})
    )


class EstoqueGasolinaCreationForm(forms.ModelForm):
    PRECOS_BASE = {
        'GAS_COMUM': Decimal('5.50'),
        'GAS_ADITIVADA': Decimal('6.20'),
        'DIESEL_COMUM': Decimal('6.00'),
        'DIESEL_S10': Decimal('6.50'),
        'ETANOL': Decimal('4.50'),
    }

    class Meta:
        model = EstoqueGasolina
        fields = ['tipo', 'quantidade_litros', 'preco_atual_litro']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_litros': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade inicial em Litros'}),
            'preco_atual_litro': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço por Litro (R$)'}),
        }

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if EstoqueGasolina.objects.filter(tipo=tipo).exists():
            raise forms.ValidationError("Este tipo de combustível já existe. Use o formulário de Movimentação para atualizá-lo.")
        return tipo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['preco_atual_litro'].initial = self.instance.preco_atual_litro
        else:
            tipo_field = self.fields.get('tipo')
            first_choice = None
            if tipo_field is not None and hasattr(tipo_field, 'choices'):
                choices = list(tipo_field.choices)
                if choices:
                    first_choice = choices[0][0]

            if first_choice and first_choice in self.PRECOS_BASE:
                self.fields['preco_atual_litro'].initial = self.PRECOS_BASE[first_choice]
            else:
                any_price = next(iter(self.PRECOS_BASE.values())) if self.PRECOS_BASE else Decimal('0.00')
                self.fields['preco_atual_litro'].initial = any_price

        self.fields['preco_atual_litro'].help_text = "Preço sugerido já preenchido. Ajuste conforme necessário."


class SimulacaoForm(forms.Form):
    item = forms.ChoiceField(
        choices=[],
        label="Item (Combustível ou Serviço)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

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
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'})
    )