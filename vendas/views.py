from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class index(View):
    retorno = 'index.html'
    def get(self, request):
        return render(request, self.retorno)

############################################
############################################
class ContaList(View):
    retorno = 'conta-list.html'
    def get(self, request):
        return render(request, self.retorno)

class ContaNew(View):
    retorno = 'conta-new.html'
    def get(self, request):
        return render(request, self.retorno)

class ContaEnd(View):
    retorno = 'conta.html'
    def get(self, request):
        return render(request, self.retorno)


############################################
############################################
class ProdutoList(View):
    retorno = 'produto-list.html'
    def get(self, request):
        return render(request, self.retorno)

class ProdutoNew(View):
    retorno = 'produto-new.html'
    def get(self, request):
        return render(request, self.retorno)

class ProdutoDell(View):
    retorno = 'produto-list.html'
    def get(self, request):
        return render(request, self.retorno)

############################################
############################################
class reports(View):
    retorno = 'reports.html'
    def get(self, request):
        return render(request, self.retorno)