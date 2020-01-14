from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.db.models import Sum

from .models import Produto, Mesa, Venda

import json
import psycopg2

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

def MesaAddProduto(request):
    retorno = ""
    id_mesa = request.POST.get('id_mesa')
    id_produto = request.POST.get('id_produto')
    quantidade = request.POST.get('quantidade')

    try:
        mesa = Mesa.objects.get(id=int(id_mesa))
        produto = Produto.objects.all().get(id=int(id_produto))

        venda = Venda(mesa=mesa, produto=produto, quantidade=quantidade)
        venda.save()
        
        retorno = {
            'succes': 'ok',
            'succes': 'ok',
            'menssagem_succes': 'Produto adicionado!',
        }

    except:
        retorno = {
            'erro': 'Erro',
            'menssagem_erro': 'Erro, tente novamente mais tarde!',
        }
    finally:
        return HttpResponse(json.dumps(retorno), content_type="application/json")


class MesaEnd(View):
    retorno = 'mesa-end.html'
    def get(self, request):

        # VARIAVEIS DO VAREJISTA
        host = 'localhost'
        dbname = 'postgres'
        port = '5432'
        username = 'postgres'
        password = 'postgres'

        try:
            # Acesar o banco
            conn = psycopg2.connect(host=host, dbname=dbname, user=username, password=password, port=port)  # Connect to an existing database
            cur = conn.cursor()  # Open a cursor to perform database operations

            select = """
            select
                vv.mesa_id, vm.apelido, vv.produto_id,
                vp.descricao as "descricao produto",
                sum(vv.quantidade) as "total quantidade",
                sum(vp.valor_unid) as "valor unidade",
                (sum(vv.quantidade) * sum(vp.valor_unid)) as "total"
            from vendas_venda vv
                inner join vendas_mesa vm on vv.mesa_id = vm.id 
                inner join vendas_produto vp on vv.produto_id  = vp.id
            where vv.mesa_id = (%s)
            group by vv.mesa_id, vm.apelido, vv.produto_id, vp.descricao
            order by vv.produto_id, vv.mesa_id;
            """
            
            # TOTAL POR PRODUTO
            cur.execute(select, (id_mesa))
            produtos_mesa = cur.fetchall()

            select = """
            select t.mesa_id, t.apelido, sum(t.total) from (
                select
                    vv.mesa_id as "mesa_id", vm.apelido as "apelido",
                    (sum(vv.quantidade) * sum(vp.valor_unid)) as "total"
                from vendas_venda vv
                    inner join vendas_mesa vm on vv.mesa_id = vm.id 
                    inner join vendas_produto vp on vv.produto_id  = vp.id
                where vv.mesa_id = (%s)
                group by vv.mesa_id, vm.apelido,
            ) t
            group by t.mesa_id, t.apelido
            order by t.mesa_id
            """

            cur.execute(select, (id_mesa))
            total = cur.fetchall()

            cur.close()
            conn.close()

            return render(request, retorno, {
                'mesa': mesa,
                'produtos_mesa': produtos_mesa,
                'total': total,
            })

        except:
            return render(request, self.retorno, {
                'mesa': None,
                'produtos_mesa': None,
                'total': None,
            })
    
    def post(self, request):
        pass

# class MesaDetail(View):
def MesaDetail(request, id_mesa):
    retorno = 'mesa.html'
    produtos_mesa = Venda.objects.all().filter(mesa__id=id_mesa).values('produto__descricao').order_by('produto__descricao').annotate(total=Sum('quantidade'))
    mesa = Mesa.objects.get(id=int(id_mesa))
    produtos = Produto.objects.all()
    try:

        return render(request, retorno, {
            'mesa': mesa,
            'produtos': produtos,
            'produtos_mesa': produtos_mesa,
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

class ProdutoEdit(View):
    retorno = 'produto-edit.html'

    def get(self, request, id_produto):
        produto = get_object_or_404(Produto, pk=id_produto)
        return render(request, self.retorno,{
            'produto': produto,
        })
    
    def post(self, request, id_produto):
        try:
            produto = get_object_or_404(Produto, pk=id_produto)
            produto.descricao = request.POST.get('produto')
            produto.valor_unid = request.POST.get('valorUnit')
            produto.save()
            
            return render(request, self.retorno, {
                'succes': 'ok',
                'menssagem_succes': 'Produto editado com sucesso!',
                'produto': produto,
            })

        except:
            
            produto = get_object_or_404(Produto, pk=id_produto)
            return render(request, self.retorno, {
                'erro': 'Erro',
                'menssagem_erro': 'Erro, tente novamente mais tarde!',
                'produto': produto,
            })
            
############################################
############################################
class reports(View):
    retorno = 'reports.html'
    def get(self, request):
        return render(request, self.retorno)