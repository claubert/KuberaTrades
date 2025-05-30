from flask import render_template, request, redirect, url_for, session, send_file, jsonify
from app.modelos import criar_usuario, verificar_usuario, criar_plano
import mercadopago
from datetime import datetime
import requests
import sys

def configurar_rotas(app):
    sdk = mercadopago.SDK("SEU_ACCESS_TOKEN_MERCADOPAGO")

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/quem_somos')
    def quem_somos():
        return render_template('quem_somos.html')

    @app.route('/planos', methods=['GET', 'POST'])
    def planos():
        if request.method == 'POST':
            tipo_plano = request.form['tipo_plano']
            session['tipo_plano'] = tipo_plano
            return redirect(url_for('login'))
        return render_template('planos.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            nome_usuario = request.form['nome_usuario']
            senha = request.form['senha']
            usuario = verificar_usuario(nome_usuario, senha)
            if usuario:
                session['usuario_id'] = usuario[0]
                # Verificar se o usuário tem um plano ativo
                cursor = app.mysql.connection.cursor()
                cursor.execute(
                    "SELECT id FROM planos WHERE usuario_id = %s AND data_fim > %s",
                    (usuario[0], datetime.now())
                )
                plano = cursor.fetchone()
                cursor.close()
                if plano:
                    # Se o usuário já tem um plano ativo, redireciona para o dashboard
                    if 'tipo_plano' in session:
                        criar_plano(usuario[0], session['tipo_plano'])
                        session.pop('tipo_plano')
                    return redirect(url_for('dashboard'))
                else:
                    # Se não tem plano, redireciona para a página de planos
                    return redirect(url_for('planos'))
            return render_template('login.html', erro="Credenciais inválidas")
        return render_template('login.html')

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            # Testar conexão com MySQL
            try:
                cursor = app.mysql.connection.cursor()
                cursor.execute("SELECT 1")
                print("Conexão com MySQL bem-sucedida!", file=sys.stderr, flush=True)
                cursor.close()
            except Exception as e:
                print(f"Erro de conexão com MySQL: {str(e)}", file=sys.stderr, flush=True)
                return render_template('cadastro.html', erro=f"Erro de conexão com MySQL: {str(e)}")

            nome_completo = request.form['nome_completo']
            cpf = request.form['cpf']
            cep = request.form['cep']
            endereco = request.form['endereco']
            nome_usuario = request.form['nome_usuario']
            email = request.form['email']
            senha = request.form['senha']
            confirmacao_senha = request.form['confirmacao_senha']
            if senha != confirmacao_senha:
                return render_template('cadastro.html', erro="As senhas não coincidem")
            try:
                criar_usuario(nome_completo, cpf, cep, endereco, nome_usuario, email, senha)
                return redirect(url_for('login'))
            except ValueError as e:
                return render_template('cadastro.html', erro=str(e))
            except Exception as e:
                return render_template('cadastro.html', erro=f"Erro ao cadastrar: {str(e)}")
        return render_template('cadastro.html')

    @app.route('/dashboard')
    def dashboard():
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        cursor = app.mysql.connection.cursor()
        cursor.execute("SELECT tipo_plano, data_fim FROM planos WHERE usuario_id = %s", (session['usuario_id'],))
        plano = cursor.fetchone()
        cursor.close()
        return render_template('dashboard.html', plano=plano)

    @app.route('/download_robot')
    def download_robot():
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return send_file('app/static/robot/robot.ex5', as_attachment=True)

    @app.route('/pagar', methods=['POST'])
    def pagar():
        tipo_plano = request.form['tipo_plano']
        valor = {'mensal': 100, 'semestral': 500, 'anual': 900}[tipo_plano]
        preferencia = {"items": [{"title": f"Plano {tipo_plano}", "quantity": 1, "unit_price": valor}],
            "external_reference": str(session.get('usuario_id', '')),"metadata": {"tipo_plano": tipo_plano}
        }
        resultado = sdk.preference().create(preferencia)
        return redirect(resultado['response']['init_point'])

    @app.route('/webhook', methods=['POST'])
    def webhook():
        dados = request.json
        if dados['action'] == 'payment.updated' and dados['data']['status'] == 'approved':
            usuario_id = dados['data']['external_reference']
            tipo_plano = dados['data']['metadata']['tipo_plano']
            criar_plano(usuario_id, tipo_plano)
        return jsonify({'status': 'ok'})

    @app.route('/api/verificar_licenca')
    def verificar_licenca():
        usuario_id = request.args.get('usuario_id')
        cursor = app.mysql.connection.cursor()
        cursor.execute("SELECT data_fim FROM planos WHERE usuario_id = %s AND data_fim > %s",(usuario_id, datetime.now()))
        plano = cursor.fetchone()
        cursor.close()
        return jsonify({'valida': bool(plano)})

    @app.route('/api/consultar_cep/<cep>')
    def consultar_cep(cep):
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            return jsonify(response.json())
        except:
            return jsonify({'erro': 'Erro ao consultar CEP'})