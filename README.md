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

## Instalação

1. Criando arquivo .env;
2. Iniciando docker;
3. Realizando migrate.

### Criando arquivo .env

```shell
sudo mv .env.dist .env
```

### Iniciando docker

```shell
docker-compose up -d
```

### Realizando migrate e collectstatic

```shell
docker-compose exec app python manage.py migrate --noinput
```

[Site](http://localhost:8000)