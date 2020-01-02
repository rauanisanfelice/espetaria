from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Produto, Mesa

class index(View):
    retorno = 'index.html'
    def get(self, request):
        return render(request, self.retorno)

############################################
############################################
class MesaList(View):
    retorno = 'mesa-list.html'
    def get(self, request):
        mesas = Mesa.objects.all().filter(data_encerramento=None)
        return render(request, self.retorno, { 'mesas': mesas })

class MesaNew(View):
    retorno = 'mesa-new.html'
    def get(self, request):
        return render(request, self.retorno)
    
    def post(self, request):
        apelido = request.POST.get('apelido')

        # VERIFICA SE APELIDO FOI PREENCHIDO
        if not apelido:
            return render(request, self.retorno, {
                'erro': 'Erro',
                'menssagem_erro': 'Campo nome vazio!',
            })

        # SALVAR NOVO PRODUTO
        try:
            modelMesa = Mesa(apelido=apelido)
            modelMesa.save()
            return render(request, self.retorno, {
                'succes': 'ok',
                'menssagem_succes': 'Mesa criada com sucesso!',
            })

        except:
            return render(request, self.retorno, {
                'erro': 'Erro',
                'menssagem_erro': 'Erro, tente novamente mais tarde!',
            })


class MesaEnd(View):
    retorno = 'mesa-list.html'
    def get(self, request):
        return render(request, self.retorno)

# class MesaDetail(View):
def MesaDetail(request, id_mesa):
    retorno = 'mesa.html'
    
    try:
        mesa = Mesa.objects.get(id=int(id_mesa))
        produtos_list = Produto.objects.all().filter(mesa_produtos__id=int(id_mesa))

        return render(request, retorno, {
            'mesa': mesa,
            'produtos': produtos_list,
        })
    except:
        return render(request, retorno, {
            'mesa': None,
            'produtos': None,
        })
    

############################################
############################################
class ProdutoList(View):
    retorno = 'produto-list.html'
    def get(self, request):
        produtos = Produto.objects.all().filter(status=True)
        return render(request, self.retorno, { 'produtos': produtos })

class ProdutoNew(View):
    retorno = 'produto-new.html'
    def get(self, request):
        return render(request, self.retorno)
    
    def post(self, request):
        descricao = request.POST.get('produto')
        valorUnit = request.POST.get('valorUnit')
        
        # VERIFICA SE DESCRICAO FOI PREENCHIDO
        if not descricao:
            return render(request, self.retorno, {
                'erro': 'Erro',
                'menssagem_erro': 'Campo descrição vazio!',
            })

        # VERIFICA SE VALOR FOI PREENCHIDO
        if not valorUnit:
            return render(request, self.retorno, {
                'erro': 'Erro',
                'menssagem_erro': 'Campo valor unitário vazio!',
            })

        # TENTA SALVAR NOVO PRODUTO
        try:
            modelProduto = Produto(descricao=descricao, valor_unid=valorUnit)
            modelProduto.save()
            return render(request, self.retorno, {
                'succes': 'ok',
                'menssagem_succes': 'Produto cadastrado com sucesso!',
            })

        except:
            return render(request, self.retorno, {
                'erro': 'Erro',
                'menssagem_erro': 'Erro, tente novamente mais tarde!',
            })

def ProdutoDell(request, id_produto):
    retorno = 'produto-list.html'

    try:
        produtoDell = Produto.objects.get(id=id_produto)
        produtoDell.status = False
        produtoDell.save()

        produtos = Produto.objects.all().filter(status=True)
        return render(request, retorno, {
            'succes': 'ok',
            'menssagem_succes': 'Produto deletado!',
            'produtos': produtos,
        })

    except:
        return render(request, retorno, {
            'erro': 'Erro',
            'menssagem_erro': 'Erro, tente novamente mais tarde!',
            'produtos': produtos,
        })


############################################
############################################
class reports(View):
    retorno = 'reports.html'
    def get(self, request):
        return render(request, self.retorno)