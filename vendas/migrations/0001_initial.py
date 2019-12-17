# Generated by Django 3.0 on 2019-12-17 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('valor_unid', models.DecimalField(decimal_places=2, max_digits=9)),
                ('data_insercao', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='mesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apelido', models.CharField(max_length=50)),
                ('quantidade', models.IntegerField(null=True)),
                ('data_lancamento', models.DateTimeField(auto_now_add=True)),
                ('data_encerramento', models.DateTimeField(null=True)),
                ('produtos', models.ManyToManyField(to='vendas.produto')),
            ],
        ),
    ]
