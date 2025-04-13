from flask import Flask, render_template
from controllers import routes
from models.database import db
import os


app = Flask(__name__, static_folder='static', template_folder='views')
app.secret_key = os.urandom(24)
routes.init_app(app)

# Permite Ler o diretório de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

#Define o nome do banco de dados
DB_NAME = 'boardgames'
app.config['DATABASE_NAME'] = DB_NAME

# Passamos o diretório ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/boardgames.sqlite3')

if __name__ == '__main__':
    # Inicializa a aplicação Flask
    db.init_app(app=app)
    with app.test_request_context():
        # Cria as tabelas
        db.create_all()
    # Inicia o aplicativo Flask
    app.run(host='localhost', port=5000, debug=True)
