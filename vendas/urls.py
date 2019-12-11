from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', index.as_view(), name='lancamento'),
    path('conta-list/', ContaList.as_view(), name='conta_list'),
    path('conta-new/', ContaNew.as_view(), name='conta_new'),
    path('conta-end/', ContaEnd.as_view(), name='conta_end'),
    path('produto-list/',ProdutoList.as_view(), name='produto_list'),
    path('produto-novo/',ProdutoNew.as_view(), name='produto_new'),
    path('produto-dell/',ProdutoDell.as_view(), name='produto_dell'),
    path('reports/', reports.as_view(), name='reports'),
]
