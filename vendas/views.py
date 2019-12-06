from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class index(View):
    retorno = 'index.html'
    def get(self, request):
        return render(request, self.retorno)

class conta(View):
    retorno = 'index.html'
    def get(self, request):
        return render(request, self.retorno)
    
class novoProduto(View):
    retorno = 'index.html'
    def get(self, request):
        return render(request, self.retorno)

class reports(View):
    retorno = 'index.html'
    def get(self, request):
        return render(request, self.retorno)