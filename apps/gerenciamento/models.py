from django.db import models
from decimal import Decimal


class EstoqueGasolina(models.Model):
    TIPOS_COMBUSTIVEL = [
        ('GAS_COMUM', 'Gasolina Comum'),
        ('GAS_ADITIVADA', 'Gasolina Aditivada'),
        ('DIESEL_COMUM', 'Diesel Comum'),
        ('DIESEL_S10', 'Diesel S-10'),
        ('ETANOL', 'Etanol'),
    ]
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_COMBUSTIVEL,
        unique=True,
        verbose_name="Tipo de Combustível"
    )
    
    quantidade_litros = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Estoque (Litros)"
    )

    preco_atual_litro = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Preço Atual por Litro (R$)"
    )

    data_ultima_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Estoque de Combustível"
        verbose_name_plural = "Estoque de Combustíveis"

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.quantidade_litros} L - R$ {self.preco_atual_litro}/L"


class RegistroCompra(models.Model):
    combustivel = models.ForeignKey(
        EstoqueGasolina,
        on_delete=models.PROTECT, 
        verbose_name='Combustível Comprado'
    )
    data_compra = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Data da Compra'
    )
    quantidade_litros = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Quantidade (L)')
    preco_compra_litro = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço de Compra por Litro (R$)')
    total_compra = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Pago (R$)')

    class Meta:
        verbose_name = 'Registro de Compra'
        verbose_name_plural = 'Registros de Compras'
        ordering = ['-data_compra'] 

    def __str__(self):
        return f"Compra: {self.combustivel.get_tipo_display()} - {self.quantidade_litros} L em {self.data_compra:%Y-%m-%d %H:%M}"


class RegistroVenda(models.Model):
    combustivel = models.ForeignKey(
        EstoqueGasolina,
        on_delete=models.PROTECT,
        verbose_name='Combustível Vendido'
    )
    data_venda = models.DateTimeField(auto_now_add=True, verbose_name='Data da Venda')
    quantidade_litros = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Quantidade (L)')
    preco_venda_litro = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço de Venda por Litro (R$)')
    total_venda = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Recebido (R$)')

    class Meta:
        verbose_name = 'Registro de Venda'
        verbose_name_plural = 'Registros de Vendas'
        ordering = ['-data_venda'] 

    def __str__(self):
        return f"Venda: {self.combustivel.get_tipo_display()} - {self.quantidade_litros} L em {self.data_venda:%Y-%m-%d %H:%M}"


class Servico(models.Model):
    nome = models.CharField(max_length=120, verbose_name='Nome do Serviço')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição') 
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Preço por Unidade (R$)')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f"{self.nome} - R$ {self.preco_unitario}"


class RegistroServico(models.Model):
    TIPO_TRANSACAO = [
        ('COMPRA', 'Compra'),
        ('VENDA', 'Venda'),
    ]

    servico = models.ForeignKey(
        Servico, 
        on_delete=models.PROTECT, 
        verbose_name='Serviço'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_TRANSACAO)
    data = models.DateTimeField(auto_now_add=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1'))
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Registro de Serviço'
        verbose_name_plural = 'Registros de Serviços'
        ordering = ['-data']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.servico.nome} - R$ {self.total} em {self.data:%Y-%m-%d %H:%M}"