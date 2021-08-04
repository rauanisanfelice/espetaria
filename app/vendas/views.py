from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from django.db.models import Sum
from django.views.generic import View, CreateView, DeleteView, UpdateView

from .models import Produto, Mesa, Venda
from .forms import ProdutoForm
from datetime import datetime

import json
import psycopg2

import logging
logger = logging.getLogger(__name__)

# VARIAVEIS DO VAREJISTA
dbname = settings.DATABASES.get('DB_NAME')
username = settings.DATABASES.get('DB_USER')
password = settings.DATABASES.get('DB_PASS')
host = settings.DATABASES.get('DB_HOST')
port = settings.DATABASES.get('DB_PORT')

class Index(View):

    retorno = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Index {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.retorno)


############################################
class MesaList(View):

    retorno = 'mesa-list.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"MesaList {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        mesas = Mesa.objects.all().filter(data_encerramento=None)
        return render(request, self.retorno, { 'mesas': mesas })

class MesaNew(View):
    retorno = 'mesa-new.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"MesaNew {request.method}")
        return super().dispatch(request, *args, **kwargs)

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

        except Exception as e:
            logger.error(f"Erro ao Salvar nova Mesa ({apelido}) - Erro: {e}")
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

    except Exception as e:
        logger.error(f"Erro ao salvar detalhes da Mesa ({id_mesa}) - Erro: {e}")
        retorno = {
            'erro': 'Erro',
            'menssagem_erro': 'Erro, tente novamente mais tarde!',
        }
    finally:
        return HttpResponse(json.dumps(retorno), content_type="application/json")


class MesaEnd(View):
    retorno = 'mesa-end.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"MesaEnd {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_mesa):
        try:
            # Acesar o banco
            conn = psycopg2.connect(host=host, dbname=dbname, user=username, password=password, port=port)
            cur = conn.cursor()

            select = """
            select
                vv.mesa_id, vm.apelido, vv.produto_id,
                vp.descricao as "descricao produto",
                sum(vv.quantidade) as "total quantidade",
                max(vp.valor_unid) as "valor unidade",
                (sum(vv.quantidade) * max(vp.valor_unid)) as "total"
            from vendas_venda vv
                inner join vendas_mesa vm on vv.mesa_id = vm.id
                inner join vendas_produto vp on vv.produto_id  = vp.id
            where vv.mesa_id = %s
            group by vv.mesa_id, vm.apelido, vv.produto_id, vp.descricao
            order by vv.produto_id, vv.mesa_id;
            """

            # TOTAL POR PRODUTO
            cur.execute(select, (id_mesa))
            produtos_mesa = cur.fetchall()
            cur.close()

            select = """
            select t.mesa_id, t.apelido, sum(t.total) from (
                select
                    vv.mesa_id as "mesa_id", vm.apelido as "apelido",
                    vv.produto_id as "produto",
                    (sum(vv.quantidade) * max(vp.valor_unid)) as "total"
                from vendas_venda vv
                    inner join vendas_mesa vm on vv.mesa_id = vm.id
                    inner join vendas_produto vp on vv.produto_id  = vp.id
                where vv.mesa_id = %s
                group by vv.mesa_id, vm.apelido, vv.produto_id
            ) t
            group by t.mesa_id, t.apelido
            order by t.mesa_id;
            """ % id_mesa

            # Acesar o banco
            cur = conn.cursor()
            cur.execute(select)
            total = cur.fetchall()

            cur.close()
            conn.close()

            mesa = Mesa.objects.get(id=int(id_mesa))
            return render(request, self.retorno, {
                'mesa': mesa,
                'produtos_mesa': produtos_mesa,
                'total': total,
            })

        except Exception as e:
            logger.error(f"Erro ao buscas dados da Mesa ({id_mesa}) - Erro: {e}")
            return render(request, self.retorno, {
                'mesa': None,
                'produtos_mesa': None,
                'total': None,
            })

    def post(self, request, id_mesa):
        mesa = Mesa.objects.get(id=int(id_mesa))
        mesa.ativo = False
        mesa.data_encerramento = datetime.today()
        mesa.save()

        return redirect('lancamento')


# class MesaDetail(View):
def MesaDetail(request, id_mesa):

    try:
        retorno = 'mesa.html'
        produtos_mesa = Venda.objects.all().filter(mesa__id=id_mesa).values('produto__descricao').order_by('produto__descricao').annotate(total=Sum('quantidade'))
        mesa = Mesa.objects.get(id=int(id_mesa))
        produtos = Produto.objects.all()

        return render(request, retorno, {
            'mesa': mesa,
            'produtos': produtos,
            'produtos_mesa': produtos_mesa,
        })
    except Exception as e:
        logger.error(f"Erro ao buscas detalhes da Mesa ({id_mesa}) - Erro: {e}")
        return render(request, retorno, {
            'mesa': None,
            'produtos': None,
        })


############################################
class ProdutoList(View):
    retorno = 'produto-list.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"ProdutoList {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        produtos = Produto.objects.all().filter(status=True)
        return render(request, self.retorno, { 'produtos': produtos })


class ProdutoNew(CreateView):

    model = Produto
    form_class = ProdutoForm
    template_name = 'produto-new.html'
    success_url = reverse_lazy('produto_list')

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"ProdutoNew {request.method}")
        return super().dispatch(request, *args, **kwargs)


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

    except Exception as e:
        logger.error(f"Erro ao salvar deletar Produto ({id_produto}) - Erro: {e}")
        return render(request, retorno, {
            'erro': 'Erro',
            'menssagem_erro': 'Erro, tente novamente mais tarde!',
            'produtos': produtos,
        })

class ProdutoEdit(View):

    retorno = 'produto-edit.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"ProdutoEdit {request.method}")
        return super().dispatch(request, *args, **kwargs)

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

        except Exception as e:
            logger.error(f"Erro ao buscar detalhes Produto ({id_produto}) - Erro: {e}")

            produto = get_object_or_404(Produto, pk=id_produto)
            return render(request, self.retorno, {
                'erro': 'Erro',
                'menssagem_erro': 'Erro, tente novamente mais tarde!',
                'produto': produto,
            })


############################################
class Reports(View):

    retorno = 'reports.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Reports {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.retorno)

class Reports_hist(View):

    retorno = 'reports-hist.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Reports_hist {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        produtos = Produto.objects.values('descricao', 'id').order_by('descricao').distinct('descricao')
        return render(request, self.retorno,{
            'produtos': produtos,
        })


def Dash_Historico(request):
    ano = request.POST.get('ano')
    id_produto = request.POST.get('id_produto')

    prefixo_select = """
    select
        EXTRACT(YEAR FROM vv.data_lancamento) as "ANO",
        EXTRACT(MONTH FROM vv.data_lancamento) as "MÊS",
        vp.descricao,
        sum(vv.quantidade) as "Volume"
    from vendas_venda vv
        inner join vendas_produto vp on vv.produto_id = vp.id
    """
    where_select = ""
    if ano or id_produto:
        where_select = " where "
        if ano:
            where_select = where_select + "EXTRACT(YEAR FROM vv.data_lancamento) = %s " % (ano)
            if id_produto:
                where_select = where_select + " AND vv.produto_id = %s " % (id_produto)
        else:
            where_select = where_select + "vv.produto_id = %s " % (id_produto)

    sufixo_select = """
        group by
            EXTRACT(YEAR FROM vv.data_lancamento),
            EXTRACT(MONTH FROM vv.data_lancamento),
            vp.descricao
        order by
            EXTRACT(YEAR FROM vv.data_lancamento),
            EXTRACT(MONTH FROM vv.data_lancamento),
            vp.descricao;
    """
    select = prefixo_select + where_select + sufixo_select

    # Acesar o banco
    conn = psycopg2.connect(host=host, dbname=dbname, user=username, password=password, port=port)
    cur = conn.cursor()

    cur.execute(select)
    qtde_historicamente = cur.fetchall()

    cur.close()
    conn.close()

    return HttpResponse(json.dumps(qtde_historicamente), content_type="application/json")


def Dash_Comparativo_Pizza(request):
    ano = request.POST.get('ano')
    mes = request.POST.get('mes')

    prefixo_select = """
    select vp.descricao, sum(vv.quantidade) as "Volume"
    from vendas_venda vv inner join vendas_produto vp on vv.produto_id = vp.id
    """
    where_select = ""
    if ano or mes:
        where_select = " where "
        if ano:
            where_select = where_select + "EXTRACT(YEAR FROM vv.data_lancamento) = %s " % (ano)
            if mes:
                where_select = where_select + " AND EXTRACT(MONTH FROM vv.data_lancamento) = %s " % (mes)
        else:
            where_select = where_select + "EXTRACT(MONTH FROM vv.data_lancamento) = %s " % (mes)

    sufixo_select = """
        group by vp.descricao
        order by 2 desc;
    """
    select = prefixo_select + where_select + sufixo_select

    # Acesar o banco
    conn = psycopg2.connect(host=host, dbname=dbname, user=username, password=password, port=port)
    cur = conn.cursor()

    cur.execute(select)
    qtde_historicamente = cur.fetchall()

    cur.close()
    conn.close()

    return HttpResponse(json.dumps(qtde_historicamente), content_type="application/json")

class Reports_comp(View):

    retorno = 'reports-comparativo.html'

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Reports_comp {request.method}")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.retorno)
