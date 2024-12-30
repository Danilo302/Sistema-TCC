from flask import Blueprint, render_template, request, session, flash, redirect, url_for,send_file, jsonify
from app.config import supabase_client
from app.routes.auth import secretaria_required

secretaria_bp = Blueprint('secretaria', __name__, url_prefix='/secretaria')

@secretaria_bp.route('/dashboard')
@secretaria_required
def dashboard():
    if 'role' in session and session['role'] == 'secretaria':
        # Carregar os pedidos dos alunos
        response = supabase_client.table('pedidos').select("*").execute()
        
        # Carregar os pedidos do aluno
        pedidos_users = response.data
        print(pedidos_users)
        
        return render_template('secretaria/dashboard.html',pedidos = pedidos_users)
        
    flash('Acesso não autorizado.', 'danger')
    return redirect(url_for('auth.login'))

@secretaria_bp.route('/detalhes_pedido/<uuid:pedido_id>', methods=['GET', 'POST'])
@secretaria_required
def detalhes_pedido(pedido_id):
    # Carregar informações do pedido
    response = supabase_client.table('pedidos').select("*").eq("id", f"{pedido_id}").execute()
    pedido_aluno = response.data[0]
    
    
    if request.method == 'POST':
        
        acao = request.form.get('acao')
        print(acao)
        if acao == 'aprovar':
            supabase_client.table('pedidos').update({'status': 'Aprovado'}).eq('id', pedido_id).execute()
            flash("Pedido aprovado com sucesso!", "success")
        elif acao == 'rejeitar':
            supabase_client.table('pedidos').update({'status': 'Rejeitado'}).eq('id', pedido_id).execute()
            flash("Pedido rejeitado com sucesso!", "success")
        return redirect(url_for('secretaria.detalhes_pedido', pedido_id=pedido_id))
    
    return render_template('secretaria/detalhes_pedido.html', pedido = pedido_aluno)
