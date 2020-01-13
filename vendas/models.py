from django.db import models

class Produto(models.Model):
    descricao = models.CharField(max_length=100)
    valor_unid = models.DecimalField(max_digits=9, decimal_places=2)
    data_insercao = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

class Mesa(models.Model):
    apelido = models.CharField(max_length=50)
    data_encerramento = models.DateTimeField(null=True)
    produtos = models.ManyToManyField(Produto, related_name='mesa_produtos')

class Venda(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField(null=True)
    data_lancamento = models.DateTimeField(auto_now_add=True)