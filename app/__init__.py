from flask import Flask
from flask_mysqldb import MySQL
from .rotas import configurar_rotas

def criar_app():
    app = Flask(__name__)
    app.config.from_object('config')

      # Configurar MySQL
    mysql = MySQL(app)
    app.mysql = mysql

      # Registrar rotas
    configurar_rotas(app)

    return app