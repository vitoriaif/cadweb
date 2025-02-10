from django import forms
from .models import *
from datetime import datetime




class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem':forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome  
    
    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem <= 0:
            raise forms.ValidationError("O campo ordem deve ser maior que zero.")
        return ordem

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if len(cpf) < 14:
            raise forms.ValidationError("O CPF deve ter pelo menos 14 caracteres.")
        return cpf

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc:
            hoje = datetime.today().date()
            if datanasc > hoje:
                raise forms.ValidationError("A data de nascimento não pode ser maior que o dia de hoje.")
            idade = hoje.year - datanasc.year - ((hoje.month, hoje.day) < (datanasc.month, datanasc.day))
            if idade < 18:
                raise forms.ValidationError("O cliente deve ter pelo menos 18 anos.")
        return datanasc    
    

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria','img_base64']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'img_base64': forms.HiddenInput(), 
            # a classe money mascara a entreda de valores monetários, está em base.html
            #  jQuery Mask Plugin
            'preco':forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }
        
        labels = {
            'nome': 'Nome do Produto',
            'preco': 'Preço do Produto',
        }


    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True 

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'qtde']

        widgets = {
            'produto': forms.HiddenInput(),
            'qtde': forms.NumberInput(attrs={
                'class': 'inteiro form-control',
                'min': 0,  # Evita valores negativos no navegador
                'placeholder': 'Digite a quantidade',
            }),
        }

    def clean_qtde(self):
        qtde = self.cleaned_data.get('qtde')
        if qtde < 0:
            raise forms.ValidationError("O valor de quantidade não pode ser negativo.")
        return qtde
  
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput(),  # Campo oculto para armazenar o ID
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido','produto', 'qtde']


        widgets = {
            'pedido': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'produto': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'qtde': forms.TextInput(attrs={'class':'inteiro form-control'}),
        }
class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pedido','forma','valor']
        widgets = {
            'pedido': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            # Usando Select para renderizar as opções
            'forma': forms.Select(attrs={'class': 'form-control'}),  
            'valor':forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
         }
        
    def __init__(self, *args, **kwargs):
            super(PagamentoForm, self).__init__(*args, **kwargs)
            self.fields['valor'].localize = True
            self.fields['valor'].widget.is_localized = True     

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        return valor