from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.config import supabase_client
from functools import wraps



# Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def aluno_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'aluno':
            flash("Acesso restrito. Faça login como aluno.", "danger")
            return redirect(url_for('auth.login'))  
        return f(*args, **kwargs)
    return decorated_function


def secretaria_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'secretaria':
            flash("Acesso restrito. Faça login como secretaria.", "danger")
            return redirect(url_for('auth.login'))  
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            response = supabase_client.table("usuarios").select("*").eq("email", f"{email}").execute()

            user_data = response.data[0]
            
            try:
                
                if user_data["senha"] == password:

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
                        #flash('Falha no login. Verifique suas credenciais.', 'danger')
                        pass
            except Exception as e:
                print('erro. senha incorreta.')
                flash('erro. senha incorreta.', 'danger')
        except Exception as e:
            print('Erro. email invalido.', 'danger')
            flash('Erro. email invalido.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        matricula = request.form.get('matricula')
        
        if password != confirm_password:
            print('As senhas não coincidem.', 'danger')
            return redirect(url_for('auth.register'))
        # Tentativa de registro no Supabase
        try:
            response = supabase_client.table('usuarios').insert({
                'nome':nome,
                'email':email,
                'senha':password,
                'tipo':'aluno',
                'matricula':matricula
            }).execute()
            
            flash('Registro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Erro ao registrar. Tente novamente.', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    # Limpar dados da sessão
    session.clear()
    flash("Você saiu!",'success')
    return redirect(url_for('auth.login'))
