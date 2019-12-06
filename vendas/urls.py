from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', index.as_view(), name='lancamento'),
    path('conta/', conta.as_view(), name='conta'),
    path('novo-produto/',novoProduto.as_view(), name='novo_produto'),
    path('reports/', reports.as_view(), name='reports'),
]
