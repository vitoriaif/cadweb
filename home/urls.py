from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView  

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('categoria/lista/',views.categoria, name="categoria"),
    path('categoria/formulario/',views.form_categoria, name="formulario"),
    path('categoria/formulario/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categoria/detalhes/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),
    path('categoria/remover/<int:id>/', views.remover_categoria, name='remover_categoria'),

## CLIENTE 

    path('cliente/', views.cliente, name="cliente"),
    path('cliente/form_cliente/', views.form_cliente, name="form_cliente"),
    path('cliente/detalhes/<int:id>/', views.detalhes_cliente, name="detalhes_cliente"),
    path('editar_cliente/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),    

##PRODUTO
    path('produto/', views.produto, name="produto"),

    path('produto/form_produto/', views.form_produto, name="form_produto"),
    path('produto/detalhes/<int:id>/', views.detalhes_produto, name="detalhes_produto"),
    path('produto/estoque/<int:id>/', views.ajustar_estoque, name="ajustar_estoque"),
    path('editar_produto/<int:id>/', views.editar_produto, name="editar_produto"),
    path('remover_produto/<int:id>', views.remover_produto, name='remover_produto'),
    path('ajustar_estoque/<int:id>', views.ajustar_estoque, name="ajustar_estoque"),
    

    ## PEDIDO 
   path('buscar_dados/<str:app_modelo>/', views.buscar_dados, name='buscar_dados'),
   path('pedido/', views.pedido, name='pedido'),
    path('pedido/novo_pedido/<int:id>', views.novo_pedido, name='novo_pedido'),
    path('pedido/detalhes/<int:id>/', views.detalhes_pedido, name='detalhes_pedido'),
    path('editar_produto/<int:id>/', views.editar_produto, name='editar_produto'),
    path('remover_pedido/<int:id>', views.remover_pedido, name='remover_pedido'),
    path('remover_item_pedido/<int:id>/', views.remover_item_pedido, name='remover_item_pedido'),
    path('editar_item_pedido/<int:id>/', views.editar_item_pedido, name='editar_item_pedido'),
    path('pagamento/editar/<int:id>/', views.editar_pagamento, name='editar_pagamento'),
    path('form_pagamento/<int:id>/', views.form_pagamento, name='form_pagamento'),
    path('remover_pagamento/<int:id>/', views.remover_pagamento, name='remover_pagamento'),
    path('notafiscal/<int:id>/', views.nota_fiscal, name='notafiscal'),
    
]