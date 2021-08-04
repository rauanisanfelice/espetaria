from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', index.as_view(), name='lancamento'),
    
    # MESAS
    path('mesa-list/', MesaList.as_view(), name='mesa_list'),
    path('mesa-new/', MesaNew.as_view(), name='mesa_new'),
    path('mesa-end/', MesaEnd.as_view(), name='mesa_end'),
    path('mesa-add-produto/', MesaAddProduto, name='mesa_add_produto'),
    path('mesa-detail/<int:id_mesa>/', MesaDetail, name='mesa_detail'),
    path('mesa-end/<int:id_mesa>/', MesaEnd.as_view(), name='mesa_end'),

    # PRODUTOS
    path('produto-list/',ProdutoList.as_view(), name='produto_list'),
    path('produto-novo/',ProdutoNew.as_view(), name='produto_new'),
    path('produto-dell/<int:id_produto>/',ProdutoDell, name='produto_dell'),
    path('produto-edit/<int:id_produto>/',ProdutoEdit.as_view(), name='produto_edit'),

    # REPORTS
    path('reports/', Reports.as_view(), name='reports'),
    path('reports-hist/', Reports_hist.as_view(), name='reports_hist'),
    path('dash-hist/', Dash_Historico, name='dash_hist'),

    path('reports-comparativo/', Reports_comp.as_view(), name='reports_comp'),
    path('dash-comp-pizza/', Dash_Comparativo_Pizza, name='dash_comp_pizza'),
]
