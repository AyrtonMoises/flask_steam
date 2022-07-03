# Flask Steam
## Features
- Busca de jogos na Steam
- Exibindo preços nas lojas do Brasil e Argentina
- Converte para real para comparar se vale a pena comprar na outra loja
- Salvar favoritos

link: [https://flask-steam.herokuapp.com/]

Prepara ambiente
```
python3 -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```
Renomear arquivo na raíz do projeto '.env.sample' para'.env' com as variáveis de ambiente
Alterar arquivo na raíz do projeto 'settings.toml' com as suas variáveis em cada tipo de ambiente

Executa migrações no banco de dados
```
flask db upgrade 
```
Inicia projeto
```
flask run
```

## Tests

```
python -m pytest --cov=flask_steam
```

### Implantação Heroku

```
Informar variáveis de ambiente na plataforma usando FLASK_NOME_VARIABLE pois o projeto utiliza o Dynaconf
```