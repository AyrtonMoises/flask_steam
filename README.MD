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
Renomear arquivos na raíz do projeto '.env_sample' para'.env' com as variáveis de ambiente e
'.flaskenv_sample' para'.flaskenv' com as variáveis de ambiente

Executa migrações no banco de dados
```
flask db upgrade 
```
Inicia projeto
```
flask run
```
