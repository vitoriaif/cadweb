import locale
from django.db import models
from decimal import Decimal


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")

    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        """Retorna a data de nascimento formatada (DD/MM/AAAA)"""
        return self.datanasc.strftime("%d/%m/%Y") if self.datanasc else None


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Melhor referenciar diretamente o modelo
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    @property
    def estoque(self):
        """Garante que um estoque esteja associado ao produto"""
        estoque_item, created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item.qtde  # Retorna apenas a quantidade para evitar problemas de acesso ao objeto


class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)  # Uso correto para um estoque único por produto
    qtde = models.IntegerField(default=0)  # Adicionando um valor padrão para evitar Null

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'

    
class Pedido(models.Model):


    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4


    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]


    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)


    def __str__(self):
            return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

    @property
    def data_pedidof(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.data_pedido:
            return self.data_pedido.strftime("%d/%m/%Y")
        return None
    
    @property
    def total(self):
        """Calcula o total de todos os itens no pedido, formatado como moeda local"""
        total = sum(item.qtde * item.preco for item in self.itempedido_set.all())
        return total

    @property
    def qtdeItens(self):
        """Conta a qtde de itens no pedido, """
        return self.itempedido_set.count()
    
    # lista de todos os pagamentos realiados
    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self) 
    
    #Calcula o total de todos os pagamentos do pedido
    @property
    def total_pago(self):
        return sum(pagamento.valor for pagamento in self.pagamentos.all())
           
    @property
    def debito(self):
        """Retorna o valor restante a ser pago no pedido."""
        return self.total - self.total_pago

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}" 
    
    @property
    def totalItem(self):
        return self.qtde * self.preco # Calcula o total de cada item
    
    
    
class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4


    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]


    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None