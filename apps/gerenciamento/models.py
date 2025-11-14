"""
Modelos do app `gerenciamento`.

Este módulo define os modelos relacionados ao estoque de combustíveis,
registro de compras/vendas e serviços oferecidos pelo posto. Os modelos
servem tanto para representar o estado atual (por exemplo, EstoqueGasolina)
quanto para manter um histórico financeiro (RegistroCompra, RegistroVenda,
RegistroServico).

Notas de uso:
- Use `EstoqueGasolina` para controlar quantidade e preço atual por litro.
- `RegistroCompra` e `RegistroVenda` são registros históricos e não devem
  ser alterados retroativamente; crie novos registros para auditoria.
"""

from django.db import models
# A biblioteca Decimal é crucial para garantir a precisão de valores monetários
# e quantidades, evitando erros comuns de ponto flutuante (float).


class EstoqueGasolina(models.Model):
    """
    Modelo principal que representa o estoque atual de cada tipo de combustível
    no posto. É aqui que se verifica a quantidade disponível e o preço de venda atual.
    """
    # Lista de tuplas (valor_interno, nome_amigável) para o campo `tipo`.
    TIPOS_COMBUSTIVEL = [
        ('GAS_COMUM', 'Gasolina Comum'),
        ('GAS_ADITIVADA', 'Gasolina Aditivada'),
        ('DIESEL_COMUM', 'Diesel Comum'),
        ('DIESEL_S10', 'Diesel S-10'),
        ('ETANOL', 'Etanol'),
    ]
    
    # Define os atributos das gasolinas
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_COMBUSTIVEL,
        unique=True, # <--- CRÍTICO: Garante que só haverá uma linha por tipo de combustível.
        verbose_name="Tipo de Combustível"
    )
    
    # Estoque atual (em Litros)
    # DecimalField é obrigatório para medidas exatas de estoque e preço.
    quantidade_litros = models.DecimalField(
        max_digits=10, # Suporta até 99.999.999,99 L (10 dígitos no total)
        decimal_places=2, # Duas casas decimais de precisão (centésimos de litro)
        default=0.00,
        verbose_name="Estoque (Litros)"
    )

    # Preço atual por litro (Preço de Venda ao Consumidor)
    preco_atual_litro = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Preço Atual por Litro (R$)"
    )

    # Timestamp automático de quando o registro foi modificado pela última vez (usado principalmente pela view de edição de preço).
    data_ultima_atualizacao = models.DateTimeField(
        auto_now=True, # Atualiza automaticamente a cada salvamento
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Estoque de Combustível"
        verbose_name_plural = "Estoque de Combustíveis"

    def __str__(self):
        # Exibe o nome amigável do tipo e o status atualizado
        return f"{self.get_tipo_display()}: {self.quantidade_litros} L - R$ {self.preco_atual_litro}/L"


class RegistroCompra(models.Model):
    """
    Modelo de registro histórico para cada compra (entrada de estoque) de combustível.
    Esses registros representam um custo para o posto.
    """
    combustivel = models.ForeignKey(
        EstoqueGasolina,
        # PROTECT: Impede a exclusão de um tipo de combustível se houver registros de compra associados.
        on_delete=models.PROTECT, 
        verbose_name='Combustível Comprado'
    )
    # Timestamp automático da criação do registro (não pode ser alterado depois).
    data_compra = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Data da Compra'
    )
    quantidade_litros = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Quantidade (L)')
    # O preço da compra é armazenado AQUI, e não no EstoqueGasolina, para fins históricos/contábeis (custo).
    preco_compra_litro = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço de Compra por Litro (R$)')
    # Total da transação de compra (quantidade * preco_compra_litro).
    total_compra = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Pago (R$)')

    class Meta:
        verbose_name = 'Registro de Compra'
        verbose_name_plural = 'Registros de Compras'
        # Ordena por data mais recente primeiro (decrescente).
        ordering = ['-data_compra'] 

    def __str__(self):
        return f"Compra: {self.combustivel.get_tipo_display()} - {self.quantidade_litros} L em {self.data_compra:%Y-%m-%d %H:%M}"


class RegistroVenda(models.Model):
    """
    Modelo de registro histórico para cada venda (saída de estoque) de combustível.
    Esses registros representam uma receita para o posto.
    """
    combustivel = models.ForeignKey(
        EstoqueGasolina,
        # PROTECT: Impede a exclusão de um tipo de combustível se houver registros de venda associados.
        on_delete=models.PROTECT,
        verbose_name='Combustível Vendido'
    )
    data_venda = models.DateTimeField(auto_now_add=True, verbose_name='Data da Venda')
    quantidade_litros = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Quantidade (L)')
    # O preço da venda é armazenado AQUI, garantindo que o registro reflita o preço daquele momento.
    preco_venda_litro = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço de Venda por Litro (R$)')
    # Total da transação de venda.
    total_venda = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Recebido (R$)')

    class Meta:
        verbose_name = 'Registro de Venda'
        verbose_name_plural = 'Registros de Vendas'
        # Ordena por data mais recente primeiro.
        ordering = ['-data_venda'] 

    def __str__(self):
        return f"Venda: {self.combustivel.get_tipo_display()} - {self.quantidade_litros} L em {self.data_venda:%Y-%m-%d %H:%M}"


class Servico(models.Model):
    """
    Modelo para definir os tipos de serviços oferecidos (ex: lavagem, troca de óleo).
    Armazena o preço unitário de venda atual.
    """
    nome = models.CharField(max_length=120, verbose_name='Nome do Serviço')
    # Campo opcional para detalhes sobre o serviço.
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição') 
    # Preço de venda atual do serviço.
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Preço por Unidade (R$)')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f"{self.nome} - R$ {self.preco_unitario}"


class RegistroServico(models.Model):
    """
    Modelo de registro histórico para transações que envolvem serviços (tanto compras de insumos
    quanto vendas de serviços ao cliente).
    """
    TIPO_TRANSACAO = [
        ('COMPRA', 'Compra'), # Custo (ex: compra de produto de limpeza)
        ('VENDA', 'Venda'),   # Receita (ex: serviço de lavagem vendido)
    ]

    servico = models.ForeignKey(
        Servico, 
        on_delete=models.PROTECT, 
        verbose_name='Serviço'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_TRANSACAO)
    data = models.DateTimeField(auto_now_add=True)
    # Quantidade de unidades vendidas/compradas (ex: 1 lavagem, 5 litros de óleo, 10 pacotes de insumo)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    # Preço unitário no momento da transação (para fins de auditoria)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    # Total da transação. Max_digits=12 permite valores de até 9.999.999.999,99
    total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Registro de Serviço'
        verbose_name_plural = 'Registros de Serviços'
        ordering = ['-data']

    def __str__(self):
        # get_tipo_display() retorna 'Compra' ou 'Venda' de forma amigável
        return f"{self.get_tipo_display()} - {self.servico.nome} - R$ {self.total} em {self.data:%Y-%m-%d %H:%M}"