from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum
from .models import *
from .forms import *
from .models import Categoria
from django.http import JsonResponse
from django.apps import apps
from django.db import transaction
from .models import Pedido, ItemPedido
from django.contrib.auth.decorators import login_required



################### CATEGORIA ################

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def categoria(request):
    contexto = {
        'lista' : Categoria.objects.all().order_by('id'),
    }
    return render(request, 'categoria/lista.html', contexto)

@login_required
def form_categoria(request):
    if request.method == 'POST':
       form = CategoriaForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            return redirect('categoria') # redireciona para a listagem
    else:# método é get, novo registro
        form = CategoriaForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)

@login_required
def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado!')
        return redirect('categoria')  # Redireciona para a listagem


    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save() # save retorna o objeto salvo
            messages.success(request, 'Operação realizada com Sucesso!')
            lista = []
            lista.append(categoria) 
            return render(request, 'categoria/lista.html', {'lista': lista})
    else:
         form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form, 'is_edit': True})

@login_required
def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado!')
        return redirect('categoria')  # Redireciona para a listagem

    if request.method == "POST":
        categoria.delete()
        messages.success(request, 'Operação realizada com Sucesso!')
        return redirect('categoria')

@login_required
def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})


###### CLIENTE ######

@login_required
def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html', contexto)
@login_required
def form_cliente(request):
    if request.method == 'POST':
       form = ClienteForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('cliente') # redireciona para a listagem
    else:# método é get, novo registro
        form = ClienteForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'cliente/formulario.html', contexto)

@login_required
def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    return render(request, 'cliente/detalhes.html', {'cliente': cliente})

@login_required
def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado!')
        return redirect('categoria')  # Redireciona para a listagem


    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save() # save retorna o objeto salvo
            messages.success(request, 'Operação realizada com Sucesso!')
            lista = []
            lista.append(cliente) 
            return render(request, 'cliente/lista.html', {'lista': lista})
    else:
         form = ClienteForm(instance=cliente)
    return render(request, 'cliente/formulario.html', {'form': form,})

@login_required
def excluir_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado!')
        return redirect('cliente')  # Redireciona para a listagem

    if request.method == "POST":
        cliente.delete()
        messages.success(request, 'Operação realizada com Sucesso!')
        return redirect('cliente')

    return render(request, 'cliente/excluir.html', {'cliente': cliente})


################### PRODUTO #######################


@login_required
def produto(request):
    contexto = {
        'lista': Produto.objects.all().order_by('-id'),
    }
    return render(request, 'produto/lista.html', contexto)

@login_required
def form_produto(request):
    if request.method == 'POST':
       form = ProdutoForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('produto') # redireciona para a listagem
    else:# método é get, novo registro
        form = ProdutoForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'produto/formulario.html', contexto)

@login_required
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto/detalhes.html', {'produto': produto})

@login_required
def editar_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado!')
        return redirect('produto')  # Redireciona para a listagem

    if request.method == 'POST':
        action = request.POST.get('action')  # Identifica a ação do botão clicado

        if action == 'save':  # Verifica se o botão "Salvar" foi clicado
            form = ProdutoForm(request.POST, instance=produto)
            if form.is_valid():
                produto = form.save()  # save retorna o objeto salvo
                messages.success(request, 'Operação realizada com Sucesso!')
                lista = [produto]
                return render(request, 'produto/lista.html', {'lista': lista})
        else:
            # Se outro botão foi clicado (como "Voltar"), não faz nada e redireciona
            return redirect('produto')  # Substitua 'categoria' pela URL desejada para "Voltar"
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto/formulario.html', {'form': form})

@login_required
def excluir_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado!')
        return redirect('produto')  # Redireciona para a listagem

    if request.method == "POST":
        produto.delete()
        messages.success(request, 'Operação realizada com Sucesso!')
        return redirect('produto')

    return render(request, 'produto/confirmar_exclusao.html', {'produto': produto})

@login_required
def ajustar_estoque(request, id):
    produto = get_object_or_404(Produto, pk=id)

    # Verifica se o produto tem um estoque, se não, cria um automaticamente
    estoque, created = Estoque.objects.get_or_create(produto=produto, defaults={'qtde': 0})

    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('produto')  # Redireciona para a listagem de produtos
        else:
            messages.error(request, 'Erro ao ajustar o estoque. Verifique os valores inseridos.')
    else:
        form = EstoqueForm(instance=estoque)

    return render(request, 'produto/estoque.html', {'form': form, 'produto': produto})

#################### PEDIDO ########################

@login_required
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

@login_required
def novo_pedido(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido_inst = form.save()
            return redirect('detalhes_pedido', id=pedido_inst.id)
        messages.error(request, 'Erro ao criar o pedido. Verifique os dados informados.')
    else:
        pedido_inst = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido_inst)
    return render(request, 'pedido/formulario.html', {'form': form})

@login_required
def remover_pedido(request, id):
    pedido_inst = get_object_or_404(Pedido, pk=id)
    with transaction.atomic():
        for item in pedido_inst.itempedido_set.all():
            item.produto.estoque.qtde += item.qtde
            item.produto.estoque.save()
        pedido_inst.delete()
    messages.success(request, "Pedido e itens removidos com sucesso!")
    return redirect('pedido')

@login_required
def detalhes_pedido(request, id):
    pedido_inst = get_object_or_404(Pedido, pk=id)
    form = ItemPedidoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item_pedido = form.save(commit=False)
        item_pedido.pedido = pedido_inst
        item_pedido.preco = item_pedido.produto.preco
        estoque = item_pedido.produto.estoque
        if item_pedido.qtde > estoque.qtde:
            messages.error(request, 'Estoque insuficiente.')
        else:
            estoque.qtde -= item_pedido.qtde
            estoque.save()
            item_pedido.save()
            messages.success(request, 'Produto adicionado ao pedido!')
        return redirect('detalhes_pedido', id=id)
    return render(request, 'pedido/detalhes.html', {'pedido': pedido_inst, 'form': form})

@login_required
def editar_item_pedido(request, id):
    item_pedido = get_object_or_404(ItemPedido, pk=id)
    pedido_inst = item_pedido.pedido
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            novo_item = form.save(commit=False)
            estoque = novo_item.produto.estoque
            if novo_item.qtde > estoque.qtde:
                messages.error(request, 'Estoque insuficiente.')
            else:
                estoque.qtde -= novo_item.qtde - item_pedido.qtde
                estoque.save()
                novo_item.save()
                messages.success(request, 'Item atualizado com sucesso!')
            return redirect('detalhes_pedido', id=pedido_inst.id)
    else:
        form = ItemPedidoForm(instance=item_pedido)
    return render(request, 'pedido/detalhes.html', {'form': form, 'pedido': pedido_inst})

@login_required
def remover_item_pedido(request, id):
    item_pedido = get_object_or_404(ItemPedido, pk=id)
    pedido_id = item_pedido.pedido.id
    item_pedido.produto.estoque.qtde += item_pedido.qtde
    item_pedido.produto.estoque.save()
    item_pedido.delete()
    messages.success(request, 'Item removido com sucesso!')
    return redirect('detalhes_pedido', id=pedido_id)

@login_required
def form_pagamento(request, id):
    pedido_inst = get_object_or_404(Pedido, pk=id)
    form = PagamentoForm(request.POST or None, instance=Pagamento(pedido=pedido_inst))
    
    # Calcular o total de pagamentos e o débito restante  
    total_pagamentos = Pagamento.objects.filter(pedido=pedido_inst).aggregate(total=Sum('valor'))['total'] or 0
    debito = pedido_inst.total - total_pagamentos
    
    # Se o método for POST, processa o pagamento
    if request.method == 'POST' and form.is_valid():
        novo_valor = form.cleaned_data['valor']
        
        # Verificar se o pagamento excede o débito restante
        if total_pagamentos + novo_valor > pedido_inst.total:
            messages.error(request, 'O valor do pagamento excede o débito restante.')
        else:
            form.save()
            messages.success(request, 'Pagamento cadastrado com sucesso!')
        return redirect('form_pagamento', id=pedido_inst.id)
    
    # Passar os valores para o template
    return render(request, 'pedido/pagamento.html', {
        'pedido': pedido_inst,
        'form': form,
        'total': pedido_inst.total,
        'total_pago': total_pagamentos,
        'debito': debito
    })

@login_required
def editar_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, pk=id)
    pedido_inst = pagamento.pedido
    form = PagamentoForm(request.POST or None, instance=pagamento)
    if request.method == 'POST' and form.is_valid():
        novo_valor = form.cleaned_data['valor']
        total_pagamentos = (Pagamento.objects.filter(pedido=pedido_inst).exclude(id=pagamento.id).aggregate(total=Sum('valor'))['total'] or 0)
        if total_pagamentos + novo_valor > pedido_inst.total:
            messages.error(request, 'O valor excede o débito restante.')
        else:
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso!')
        return redirect('editar_pagamento', id=pagamento.id)
    return render(request, 'pedido/pagamento.html', {'form': form, 'pedido': pedido_inst})

@login_required
def remover_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, pk=id)
    pedido_id = pagamento.pedido.id
    pagamento.delete()
    messages.success(request, 'Pagamento removido com sucesso!')
    return redirect('form_pagamento', id=pedido_id)

