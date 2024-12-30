from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.config import supabase_client
from functools import wraps



# Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def aluno_required(f):
    """Decorator para verificar se o usuário é um aluno."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'aluno':
            flash("Acesso restrito. Faça login como aluno.", "danger")
            return redirect(url_for('auth.login'))  # Redireciona para a página de login
        return f(*args, **kwargs)
    return decorated_function


def secretaria_required(f):
    """Decorator para verificar se o usuário é da secretaria."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'secretaria':
            flash("Acesso restrito. Faça login como secretaria.", "danger")
            return redirect(url_for('login'))  # Redireciona para a página de login
        return f(*args, **kwargs)
    return decorated_function


#Rota para teste
@auth_bp.route('/listar', methods=['GET'])
def listar():
    try:
        # Fazendo a consulta à tabela "usuarios"
        response = supabase_client.table('usuarios').select('*').execute()

        # Verifica se há dados retornados
        if response.data:
            return jsonify(response.data), 200  # Retorna os dados e o status 200 (sucesso)
        else:
            return jsonify({"message": "Nenhum usuário encontrado"}), 404
    except Exception as e:
        # Captura erros e retorna com um status 500 (erro interno do servidor)
        return jsonify({"error": str(e)}), 500



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        

        # Tentativa de login no Supabase
        try:
            response = supabase_client.table("usuarios").select("*").eq("email", f"{email}").execute()

            print(response.data[0])
            user_data = response.data[0]
            
            try:
                #corrigir isso
                
                if user_data["senha"] == password:
                    print(response.data[0])
                    

                    if user_data:
                        # Configurar dados da sessão
                        session['user_id'] = user_data['id']
                        session['nome'] = user_data['nome']
                        session['email'] = user_data['email']
                        session['role'] = user_data['tipo']  

                        # Redireciona baseado no tipo de usuário
                        if session['role'] == 'aluno':
                            return redirect(url_for('aluno.dashboard'))
                        elif session['role'] == 'secretaria':
                            return redirect(url_for('secretaria.dashboard'))
                    else:
                        flash('Falha no login. Verifique suas credenciais.', 'danger')
            except Exception as e:
                print('erro. senha incorreta.')
        except Exception as e:
            print('Erro. email invalido.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')  # 'aluno' ou 'secretaria'

        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('auth.register'))

        # Tentativa de registro no Supabase
        try:
            response = supabase_client.auth.sign_up(
                email=email,
                password=password,
                user_metadata={'role': role}
            )
            flash('Registro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Erro ao registrar. Tente novamente.', 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    # Limpar dados da sessão
    session.clear()
    flash('Você saiu do sistema.', 'success')
    return redirect(url_for('auth.login'))
