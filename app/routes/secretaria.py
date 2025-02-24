from flask import Blueprint, render_template, request, session, flash, redirect, url_for,send_file, jsonify
from app.config import supabase_client
from app.routes.auth import secretaria_required

secretaria_bp = Blueprint('secretaria', __name__, url_prefix='/secretaria')

@secretaria_bp.route('/dashboard')
@secretaria_required
def dashboard():
    if 'role' in session and session['role'] == 'secretaria':
        # Carregar os pedidos dos alunos
        response = supabase_client.table('pedidos_roa').select("*").execute()
        # Carregar os pedidos do aluno
        pedidos_users = response.data
        
        aluno_response = supabase_client.table('usuarios').select("id, nome").execute()
        alunos = aluno_response.data
        
        ficha_response = supabase_client.table('ficha_catalografica').select("*").execute()
        fichasCatalograficas = ficha_response.data
        
        for aluno in alunos:
            for pedido in pedidos_users:
                if aluno['id'] == pedido['id_aluno']:
                    pedido['nome_aluno'] = aluno['nome']
                for ficha in fichasCatalograficas:
                    if pedido['id_aluno'] == ficha['id_aluno']:
                        pedido['ficha'] = ficha['id']
        return render_template('secretaria/dashboard.html',pedidos = pedidos_users,alunos = aluno_response, fichas = fichasCatalograficas)
        
    flash('Acesso não autorizado.', 'danger')
    return redirect(url_for('auth.login'))

@secretaria_bp.route('/detalhes_pedido/<uuid:pedido_id>', methods=['GET', 'POST'])
@secretaria_required
def detalhes_pedido(pedido_id):
    # Carregar informações do pedido
    response = supabase_client.table('pedidos_roa').select("*").eq("id", f"{pedido_id}").execute()
    pedido_aluno = response.data[0]
    
    if pedido_aluno:
        # Obter o id_aluno associado ao pedido
        id_aluno = pedido_aluno['id_aluno']
        
        # Consultar informações do aluno
        aluno_response = supabase_client.table('usuarios').select("matricula, nome").eq("id", id_aluno).execute()
        aluno = aluno_response.data[0] if aluno_response.data else None
    
    if request.method == 'POST':
        
        obs = request.form.get('obs')
        if obs :
            supabase_client.table('pedidos_roa').update({'obs': obs}).eq('id', pedido_id).execute()
            flash("Justificativa enviada com sucesso!")
        acao = request.form.get('acao')
        print(acao)
        if acao == 'aprovar':
            supabase_client.table('pedidos_roa').update({'status': 'Aprovado'}).eq('id', pedido_id).execute()
            flash("Pedido aprovado com sucesso!", "success")
        elif acao == 'reprovar':
            supabase_client.table('pedidos_roa').update({'status': 'Reprovado'}).eq('id', pedido_id).execute()
            flash("Pedido reprovado com sucesso!", "success")
        return redirect(url_for('secretaria.detalhes_pedido', pedido_id=pedido_id))
    
    return render_template('secretaria/detalhes_pedido.html', pedido = pedido_aluno, aluno=aluno)

@secretaria_bp.route('/ficha_catalografica/<uuid:ficha_id>', methods=['GET', 'POST'])
@secretaria_required
def ficha_catalografica(ficha_id):
    response = supabase_client.table('ficha_catalografica').select("*").eq("id", f"{ficha_id}").execute()
    ficha_catalografica_aluno = response.data[0]
    id_aluno = ficha_catalografica_aluno['id_aluno']
    
    aluno_response = supabase_client.table('usuarios').select("matricula, nome").eq("id", id_aluno).execute()
    aluno = aluno_response.data[0] if aluno_response.data else None
    return render_template('secretaria/ficha_catalografica_aluno.html', ficha = ficha_catalografica_aluno, aluno = aluno)