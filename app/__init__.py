from flask import Flask
from flask_mysqldb import MySQL
from .rotas import configurar_rotas
import sys

def criar_app():
    app = Flask(__name__)

    # Carregar configurações de config.py
    try:
        app.config.from_object('config')
        print(f"Configurações carregadas: SECRET_KEY={app.config.get('SECRET_KEY')}, MYSQL_USER={app.config.get('MYSQL_USUARIO')}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"Erro ao carregar config.py: {str(e)}", file=sys.stderr, flush=True)
        raise

    # Configurações explícitas para MySQL
    app.config['MYSQL_USER'] = app.config.get('MYSQL_USUARIO', 'root')
    app.config['MYSQL_PASSWORD'] = app.config.get('MYSQL_SENHA', 'Controle@22')
    app.config['MYSQL_HOST'] = app.config.get('MYSQL_HOST', 'localhost')
    app.config['MYSQL_DB'] = app.config.get('MYSQL_BANCO', 'kuberatrades')

    # Garantir que a SECRET_KEY esteja definida
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = app.config.get('CHAVE_SECRETA', '2124sdfs554121')
        print(f"SECRET_KEY definida como: {app.config['SECRET_KEY']}", file=sys.stderr, flush=True)

    # Inicializar MySQL
    mysql = MySQL(app)
    app.mysql = mysql

    # Testar conexão dentro de um contexto de aplicação
    with app.app_context():
        try:
            cursor = app.mysql.connection.cursor()
            cursor.execute("SELECT 1")
            print("Conexão com MySQL bem-sucedida!", file=sys.stderr, flush=True)
            cursor.close()
        except Exception as e:
            print(f"Erro de conexão com MySQL: {str(e)}", file=sys.stderr, flush=True)

    # Registrar rotas
    configurar_rotas(app)

    return app