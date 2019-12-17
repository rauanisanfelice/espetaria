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
    path('mesa-detail/', MesaDetail.as_view(), name='mesa_detail'),

    # PRODUTOS
    path('produto-list/',ProdutoList.as_view(), name='produto_list'),
    path('produto-novo/',ProdutoNew.as_view(), name='produto_new'),
    path('produto-dell/<int:id_produto>/',ProdutoDell, name='produto_dell'),

    # REPORTS
    path('reports/', reports.as_view(), name='reports'),
]
