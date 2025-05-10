from flask import Flask
from flask_mysqldb import MySQL
from .rotas import configurar_rotas
import sys

def criar_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Configurações explícitas para garantir que sejam usadas
    app.config['MYSQL_USER'] = app.config.get('MYSQL_USUARIO', 'root')
    app.config['MYSQL_PASSWORD'] = app.config.get('MYSQL_SENHA', 'Controle@22')
    app.config['MYSQL_HOST'] = app.config.get('MYSQL_HOST', 'localhost')
    app.config['MYSQL_DB'] = app.config.get('MYSQL_BANCO', 'kuberatrades')

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