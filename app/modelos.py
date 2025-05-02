from flask import current_app
import hashlib
from datetime import datetime, timedelta
import re

def validar_cpf(cpf):
    # Remove pontos e traços
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    # Validação dos dígitos verificadores
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    resto = total % 11
    digito1 = 0 if resto < 2 else 11 - resto
    if int(cpf[9]) != digito1:
        return False
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    resto = total % 11
    digito2 = 0 if resto < 2 else 11 - resto
    return int(cpf[10]) == digito2

def criar_usuario(nome_completo, cpf, cep, endereco, nome_usuario, email, senha):
    if not validar_cpf(cpf):
        raise ValueError("CPF inválido")
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    cursor = current_app.mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome_completo, cpf, cep, endereco, nome_usuario, email, senha) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nome_completo, cpf, cep, endereco, nome_usuario, email, senha_hash)
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