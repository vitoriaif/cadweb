import locale
from django.db import models
from decimal import Decimal
import random



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
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None

    @property 
    def total(self):
        """Retorna o total do pedido como Decimal"""
        total = sum(item.qtde * item.preco for item in self.itempedido_set.all())
        return Decimal(total)  

    @property
    def icms(self):
        """ICMS: 18% sobre o total do pedido."""
        return self.total * Decimal(0.18)

    @property
    def ipi(self):
        """IPI: 5% sobre o total do pedido."""
        return self.total * Decimal(0.05)

    @property
    def pis(self):
        """PIS: 1.65% sobre o total do pedido."""
        return self.total * Decimal(0.0165)

    @property
    def cofins(self):
        """COFINS: 7.6% sobre o total do pedido."""
        return self.total * Decimal(0.076)

    @property
    def impostos_totais(self):
        """Soma de todos os impostos."""
        return self.icms + self.ipi + self.pis + self.cofins

    @property
    def valor_final(self):
        """Valor final do pedido considerando os impostos."""
        return self.total + self.impostos_totais

    @property
    def qtdeItens(self):
        return self.itempedido_set.count()

    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self)

    @property
    def total_pago(self):
        total = sum(pagamento.valor for pagamento in self.pagamentos.all())
        return Decimal(total)  

    @property
    def debito(self):
        valor_debito = self.total - self.total_pago 
        return Decimal(valor_debito)  

    @property
    def chave_acesso(self):
        """Gera uma chave de acesso única baseada no ID do pedido e na data do pedido."""
        if not self.data_pedido or not self.id:
            return None
        
         # Data de emissão no formato YYYYMMDD
        data_formatada = self.data_pedido.strftime('%Y%m%d')
        
        # ID do pedido com no mínimo 6 dígitos (ex: 000123)
        id_pedido = str(self.id).zfill(6)
        
        # Gera números aleatórios para completar até 44 caracteres
        restante = 44 - (len(data_formatada) + len(id_pedido))
        numeros_aleatorios = ''.join(str(random.randint(0, 9)) for _ in range(restante))
        
        # Monta a chave numérica final
        chave = f"{data_formatada}{id_pedido}{numeros_aleatorios}"
        return chave

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} (Qtde: {self.qtde}) - Preço Unitário: {self.preco}"
    
    @property
    def calculoTotal(self):
        """Calcula o total do item considerando a quantidade e o preço"""
        total = self.qtde * self.preco
        return Decimal(total)  # Certifique-se de que o total seja um Decimal


class Pagamento(models.Model):
    DINHEIRO = 1
    CREDITO = 2
    DEBITO = 3
    PIX = 4
    TICKET = 5
    OUTRA = 6

    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CREDITO, 'Credito'),
        (DEBITO, 'Debito'),
        (PIX, 'Pix'),
        (TICKET, 'Ticket'),
        (OUTRA, 'Outra'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE) 
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits = 10, decimal_places=2, blank = False )
    data_pgto = models.DateTimeField(auto_now_add=True)

    @property
    def data_pgtof(self):
        """Retorna a data formatada: DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None
