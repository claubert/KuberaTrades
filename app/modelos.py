from flask import current_app
import hashlib
from datetime import datetime, timedelta

def criar_usuario(nome_usuario, senha, email):
      senha_hash = hashlib.sha256(senha.encode()).hexdigest()
      cursor = current_app.mysql.connection.cursor()
      cursor.execute(
          "INSERT INTO usuarios (nome_usuario, senha, email) VALUES (%s, %s, %s)",
          (nome_usuario, senha_hash, email)
      )
      current_app.mysql.connection.commit()
      cursor.close()

def verificar_usuario(nome_usuario, senha):
      senha_hash = hashlib.sha256(senha.encode()).hexdigest()
      cursor = current_app.mysql.connection.cursor()
      cursor.execute(
          "SELECT id FROM usuarios WHERE nome_usuario = %s AND senha = %s",
          (nome_usuario, senha_hash)
      )
      usuario = cursor.fetchone()
      cursor.close()
      return usuario

def criar_plano(usuario_id, tipo_plano):
      data_inicio = datetime.now()
      if tipo_plano == 'mensal':
          data_fim = data_inicio + timedelta(days=30)
      elif tipo_plano == 'semestral':
          data_fim = data_inicio + timedelta(days=180)
      else:
          data_fim = data_inicio + timedelta(days=365)

      cursor = current_app.mysql.connection.cursor()
      cursor.execute(
          "INSERT INTO planos (usuario_id, tipo_plano, data_inicio, data_fim) VALUES (%s, %s, %s, %s)",
          (usuario_id, tipo_plano, data_inicio, data_fim)
      )
      current_app.mysql.connection.commit()
      cursor.close()