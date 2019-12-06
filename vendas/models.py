from django.db import models

class produto(models.Model):
    descricao = models.CharField(max_length=100)
    valor_unid = models.DecimalField(max_digits=9, decimal_places=2)
    data_insercao = models.DateField(auto_now=True)

    cho_status = [
        ('at', 'ativo'),
        ('ex', 'deletado'),
    ]
    status = models.CharField(max_length=2, choices=cho_status, default=cho_status[0][0])

    class Meta:
        db_table = 'produto'
        verbose_name_plural = 'produtos'

class venda(models.Model):
    apelido = models.CharField(max_length=50)
    produto = models.ForeignKey(produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    data_lancamento = models.DateTimeField(auto_now_add=True)

    cho_status = [
        ('on', 'ativa'),
        ('of', 'fechada'),
    ]
    status = models.CharField(max_length=2, choices=cho_status, default=cho_status[0][0])

    class Meta:
        db_table = 'venda'
        verbose_name_plural = 'vendas'