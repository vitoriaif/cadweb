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
        'lista': Produto.objects.all().order_by('id'),
    }
    return render(request, 'produto/lista.html',contexto)
@login_required
def form_produto(request):
    if request.method == 'POST':
       form = ProdutoForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, "Produto adicionado com sucesso!")
            return redirect('produto') # redireciona para a listagem
    else:# método é get, novo registro
        form = ProdutoForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'produto/formulario.html', contexto)
@login_required
def editar_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        preco_original = produto.preco  # Guarda o preço original antes da edição
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            novo_preco = form.cleaned_data.get('preco')
            if novo_preco != preco_original:
                # Força a atualização via signal
                produto = form.save()
                messages.success(request, 'Preço atualizado nos pedidos!')
            else:
                produto.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('produto')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produto/formulario.html', {'form': form})
@login_required
def remover_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')  # Redireciona para a listagem
    
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Operação realizada com Sucesso')
        return redirect('produto')  # Redireciona para a listagem
    
    # Se for um GET, renderiza a página de confirmação
    return render(request, 'produto/excluir.html', {'produto': produto})
@login_required
def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        messages.error(request, "Registro não encontrado.")
        return redirect('produto')  # Redireciona para a listagem
    return render(request, 'produto/detalhes.html', {'produto': produto})
@login_required
def ajustar_estoque(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        estoque = produto.estoque  # pega o objeto estoque relacionado ao produto
    except Produto.DoesNotExist:
        messages.error(request, "Registro não encontrado.")
        return redirect('produto')
    
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = [estoque.produto]
            messages.success(request, "Operação realizada com sucesso.")
            return render(request, 'produto/lista.html', {'lista': lista})
    else:
        form = EstoqueForm(instance=estoque)

    return render(request, 'produto/estoque.html', {'form': form})


@login_required
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})
@login_required
def novo_pedido(request,id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            # Caso o registro não seja encontrado, exibe a mensagem de erro
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente')  # Redireciona para a listagem
        # cria um novo pedido com o cliente selecionado
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)# cria um formulario com o novo pedido
        return render(request, 'pedido/formulario.html',{'form': form,})
    else: # se for metodo post, salva o pedido.
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('detalhes_pedido', id=pedido.id)
@login_required        
def remover_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, "Pedido não encontrado.")
        return redirect('pedido')

    with transaction.atomic():
        # Altere "itens" para "itempedido_set" (padrão do Django)
        for item in pedido.itempedido_set.all():
            produto = item.produto
            quantidade = item.qtde
            estoque = produto.estoque
            estoque.qtde += quantidade
            estoque.save()

        pedido.delete()

    messages.success(request, "Pedido e itens removidos com sucesso!")
    return redirect('pedido')
@login_required
def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else:
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.pedido = pedido
            item_pedido.preco = item_pedido.produto.preco

            produto = item_pedido.produto
            estoque = produto.estoque

            # Verifica se o produto já existe no pedido
            existing_item = pedido.itempedido_set.filter(produto=produto).first()
            if existing_item:
                # Atualiza a quantidade do item existente
                if item_pedido.qtde > estoque.qtde:
                    messages.error(request, 'Estoque insuficiente para adicionar esta quantidade.')
                    return redirect('detalhes_pedido', id=id)
                existing_item.qtde += item_pedido.qtde
                existing_item.save()
                # Atualiza o estoque
                estoque.qtde -= item_pedido.qtde
                estoque.save()
                messages.success(request, 'Quantidade do produto atualizada no pedido!')
            else:
                # Cria um novo item
                if item_pedido.qtde > estoque.qtde:
                    messages.error(request, 'Estoque insuficiente para este produto')
                    return redirect('detalhes_pedido', id=id)
                # Atualiza estoque
                estoque.qtde -= item_pedido.qtde
                estoque.save()
                # Salva item do pedido
                item_pedido.save()
                messages.success(request, 'Produto adicionado ao pedido com sucesso!')
            return redirect('detalhes_pedido', id=id)
        else:
            messages.error(request, 'Erro ao adicionar produto')

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html', contexto)
@login_required
def editar_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        messages.error(request, "Registro não encontrado")
        return redirect('pedido')  # Redirecionamento 

    pedido = item_pedido.pedido
    produto_anterior = item_pedido.produto
    quantidade_anterior = item_pedido.qtde

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            novo_item_pedido = form.save(commit=False)
            novo_produto = novo_item_pedido.produto
            nova_quantidade = novo_item_pedido.qtde

            with transaction.atomic():
                # Caso 1: Produto não foi alterado (mesmo produto)
                if novo_produto == produto_anterior:
                    diferenca_quantidade = nova_quantidade - quantidade_anterior
                    estoque = produto_anterior.estoque

                    if diferenca_quantidade > estoque.qtde:
                        messages.error(request, 'Estoque insuficiente para esta alteração.')
                        return redirect('detalhes_pedido', id=pedido.id)

                    # Atualiza estoque e quantidade
                    estoque.qtde -= diferenca_quantidade
                    estoque.save()
                    novo_item_pedido.save()

                # Caso 2: Produto foi alterado
                else:
                    # Verifica se o novo produto já existe no pedido (exceto o item atual)
                    existing_item = pedido.itempedido_set.filter(produto=novo_produto).exclude(id=item_pedido.id).first()
                    estoque_novo = novo_produto.estoque
                    estoque_anterior = produto_anterior.estoque

                    # Caso 2a: Novo produto já existe no pedido
                    if existing_item:
                        if nova_quantidade > estoque_novo.qtde:
                            messages.error(request, 'Estoque insuficiente para adicionar esta quantidade.')
                            return redirect('detalhes_pedido', id=pedido.id)

                        # Atualiza o item existente
                        existing_item.qtde += nova_quantidade
                        existing_item.save()

                        # Restaura estoque do produto anterior
                        estoque_anterior.qtde += quantidade_anterior
                        estoque_anterior.save()

                        # Deduz estoque do novo produto
                        estoque_novo.qtde -= nova_quantidade
                        estoque_novo.save()

                        # Remove o item editado (pois foi mesclado)
                        item_pedido.delete()

                    # Caso 2b: Novo produto não existe no pedido
                    else:
                        if nova_quantidade > estoque_novo.qtde:
                            messages.error(request, 'Estoque insuficiente para este produto.')
                            return redirect('detalhes_pedido', id=pedido.id)

                        # Restaura estoque do produto anterior
                        estoque_anterior.qtde += quantidade_anterior
                        estoque_anterior.save()

                        # Deduz estoque do novo produto
                        estoque_novo.qtde -= nova_quantidade
                        estoque_novo.save()

                        # Atualiza o item com novo produto e preço
                        novo_item_pedido.preco = novo_produto.preco
                        novo_item_pedido.save()

                messages.success(request, 'Item do pedido atualizado com sucesso!')
                return redirect('detalhes_pedido', id=pedido.id)
        else:
            messages.error(request, 'Erro ao atualizar o item do pedido.')

    else:
        form = ItemPedidoForm(instance=item_pedido)

    contexto = {
        'form': form,
        'item_pedido': item_pedido,
        'pedido': pedido
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)
    
    pedido_id = item_pedido.pedido.id  # Armazena o ID do pedido antes de remover o item
    estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
    estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
    estoque.save()  # Salva as alterações no estoque
    # Remove o item do pedido
    item_pedido.delete()
    messages.success(request, 'Operação realizada com Sucesso')


    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhes_pedido', id=pedido_id)
@login_required
def form_pagamento(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido não encontrado')
        return redirect('pedido')

    if request.method == 'POST':
        # Create a payment instance linked to the order
        pagamento = Pagamento(pedido=pedido)
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            # Calculate total payments including the new one
            total_pagamentos = Pagamento.objects.filter(pedido=pedido).aggregate(total=Sum('valor'))['total'] or 0
            novo_valor = form.cleaned_data['valor']
            total_com_novo = total_pagamentos + novo_valor

            if total_com_novo > pedido.total:
                messages.error(request, 'O valor do pagamento excede o débito restante.')
            else:
                form.save()
                messages.success(request, 'Pagamento cadastrado com sucesso!')
                return redirect('form_pagamento', id=pedido.id)
        else:
            messages.error(request, 'Erro no formulário.')
    else:
        # GET request: prepare a new payment form
        form = PagamentoForm(instance=Pagamento(pedido=pedido))

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/pagamento.html', contexto)
@login_required
def editar_pagamento(request, id):
    try:
        pagamento = Pagamento.objects.get(pk=id)
    except Pagamento.DoesNotExist:
        messages.error(request, 'Pagamento não encontrado')
        return redirect('pedido')

    pedido = pagamento.pedido

    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            novo_valor = form.cleaned_data['valor']
            # Calcular o total de pagamentos realizados, excluindo o pagamento que está sendo editado
            total_pagamentos = Pagamento.objects.filter(pedido=pedido).exclude(id=pagamento.id).aggregate(total=Sum('valor'))['total'] or 0

            # Somar com o novo pagamento
            total_com_novo = total_pagamentos + novo_valor

            if total_com_novo > pedido.total:
                messages.error(request, 'O valor excede o débito restante.')
            else:
                form.save()
                messages.success(request, 'Pagamento atualizado com sucesso!')
                return redirect('editar_pagamento', id=pagamento.id)
        else:
            messages.error(request, 'Erro no formulário.')
    else:
        form = PagamentoForm(instance=pagamento)

    contexto = {
        'form': form,
        'pagamento': pagamento,
        'pedido': pedido,
    }
    return render(request, 'pedido/pagamento.html', contexto)
@login_required
def remover_pagamento(request, id):
    try:
        pagamento = Pagamento.objects.get(pk=id)
    except Pagamento.DoesNotExist:
        messages.error(request, 'Pagamento não encontrado')
        return redirect('pedido')

    pedido_id = pagamento.pedido.id
    pagamento.delete()
    messages.success(request, 'Pagamento removido com sucesso!')
    return redirect('form_pagamento', id=pedido_id)
def nota_fiscal(request, id):
    try:
        # Tenta buscar o pedido pelo ID
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        # Retorna uma página de erro personalizada ou uma mensagem amigável
        messages.error(request, 'Pedido não encontrado')
        return redirect('pedido')

    # Renderiza o template passando o pedido como contexto
    return render(request, 'pedido/notafiscal.html', {'pedido': pedido})