from django.db import models

class produto(models.Model):
    descricao = models.CharField(max_length=100)
    valor_unid = models.DecimalField(max_digits=9, decimal_places=2)
    data_insercao = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

class mesa(models.Model):
    apelido = models.CharField(max_length=50)
    quantidade = models.IntegerField()
    data_lancamento = models.DateTimeField(auto_now_add=True)
    data_encerramento = models.DateTimeField(auto_now_add=True)
    produtos = models.ManyToManyField(produto)