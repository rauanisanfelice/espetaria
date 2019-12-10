![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/rauanisanfelice/espetaria.svg)
![GitHub top language](https://img.shields.io/github/languages/top/rauanisanfelice/espetaria.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/rauanisanfelice/espetaria.svg)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/rauanisanfelice/espetaria)
![GitHub contributors](https://img.shields.io/github/contributors/rauanisanfelice/espetaria.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/rauanisanfelice/espetaria.svg)

![GitHub stars](https://img.shields.io/github/stars/rauanisanfelice/espetaria.svg?style=social)
![GitHub followers](https://img.shields.io/github/followers/rauanisanfelice.svg?style=social)
![GitHub forks](https://img.shields.io/github/forks/rauanisanfelice/espetaria.svg?style=social)

# Espetaria

Sistema de controle de saídas de espetinhos.

## Instalação:

1. Ambiente Python;
2. Instalando dependências;
3. Inicialização dos container;
    1. Configurando o pgAdmin;
4. Iniciar o servidor.

### Ambiente Python:

```
virtualenv -p python3 env
source env/bin/activate
```

### Instalando dependências:
```
pip3 install -r requirements.txt
```

### Inicialização dos container

```
docker-compose up -d
```

#### Configurando o pgAdmin;

Acesse o link:

[pgAdmin](http://localhost:80)

Realize o login:
>User: admin  
>Pass: admin

Clique em: Create >> Server

Conecte no Banco com os seguintes parametros:  

Name: #nome desejado#  
>Host: espetaria-postgre
>Port: 5432  
>DB  : postgres  
>User: postgres  
>Pass: docker123

### Iniciar o servidor.

```
python manage.py runserver 8000 --noreload
```

[Site](http://localhost:8000)