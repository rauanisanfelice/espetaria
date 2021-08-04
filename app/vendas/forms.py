from django.forms import ModelForm
from .models import Produto


class ProdutoForm(ModelForm):

    class Meta:
        model = Produto
        fields = ['descricao', 'valor_unid']

        help_texts = {
            'valor_unid': 'Exemplo: 99.99',
        }
        error_messages = {
            'descricao': {
                'null': 'Campo obrigatório',
                'blank': 'Campo obrigatório',
                'required': 'Campo obrigatório',
            },
            'valor_unid': {
                'null': 'Campo obrigatório',
                'blank': 'Campo obrigatório',
                'required': 'Campo obrigatório',
            },
        }