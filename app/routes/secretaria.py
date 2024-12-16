from flask import Blueprint, render_template, request, session, flash, redirect, url_for

secretaria_bp = Blueprint('secretaria', __name__, url_prefix='/secretaria')

@secretaria_bp.route('/dashboard')
def dashboard():
    if 'role' in session and session['role'] == 'secretaria':
        # Carregar os pedidos dos alunos
        return render_template('secretaria/dashboard.html')
    flash('Acesso não autorizado.', 'danger')
    return redirect(url_for('auth.login'))

@secretaria_bp.route('/detalhes_pedido/<int:pedido_id>')
def detalhes_pedido(pedido_id):
    # Carregar informações do pedido
    return render_template('secretaria/detalhes_pedido.html', pedido_id=pedido_id)
