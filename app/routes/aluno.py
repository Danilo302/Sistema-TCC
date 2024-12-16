from flask import Blueprint, render_template, request, redirect, url_for, session, flash

aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')

@aluno_bp.route('/dashboard')
def dashboard():
    if 'role' in session and session['role'] == 'aluno':
        # Carregar os pedidos do aluno
        return render_template('aluno/dashboard.html')
    flash('Acesso não autorizado.', 'danger')
    return redirect(url_for('auth.login'))

@aluno_bp.route('/cadastrar_pedido', methods=['GET', 'POST'])
def cadastrar_pedido():
    if request.method == 'POST':
        # Salvar pedido no banco de dados
        
        
        flash('Pedido cadastrado com sucesso!', 'success')
        return redirect(url_for('aluno.dashboard'))
    return render_template('aluno/cadastrar_pedido.html')
