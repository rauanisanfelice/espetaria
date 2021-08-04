from django.test import TestCase
from .models import Produto, Venda, Mesa
from .forms import ProdutoForm



class ProdutoTestCase(TestCase):

    def setUp(self):
        Produto.objects.create(descricao="Queijo", valor_unid=9.99)
        Produto.objects.create(descricao="Picanha", valor_unid=100.00)

    def test_produto_criado(self):
        """Teste se os produtos foram criados"""
        produto_01 = Produto.objects.get(descricao="Queijo")
        produto_02 = Produto.objects.get(descricao="Picanha")
        self.assertIsNotNone(produto_01)
        self.assertIsNotNone(produto_02)

class FormProdutoErrosTestCase(TestCase):

    def test_produto_descricao_null(self):
        """Teste erro descrição null"""

        error_message = "{'descricao': [{'message': 'Campo obrigatório', 'code': 'required'}]}"
        data = {"descricao": None, "valor_unid": 9.99 }
        form = ProdutoForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(str(form.errors.get_json_data(escape_html=False)), error_message)

    def test_produto_valor_null(self):
        """Teste erro valor unitario null"""

        error_message = "{'valor_unid': [{'message': 'Campo obrigatório', 'code': 'required'}]}"
        data = {"descricao": "Peixe", "valor_unid": None }
        form = ProdutoForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(str(form.errors.get_json_data(escape_html=False)), error_message)

    def test_produto_erros_null(self):
        """Teste erro valor unitario null"""

        error_message = "{'descricao': [{'message': 'Campo obrigatório', 'code': 'required'}], 'valor_unid': [{'message': 'Campo obrigatório', 'code': 'required'}]}"
        data = {"descricao": None, "valor_unid": None }
        form = ProdutoForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(str(form.errors.get_json_data(escape_html=False)), error_message)