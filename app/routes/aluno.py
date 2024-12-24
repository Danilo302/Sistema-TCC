from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import supabase
from app.config import SUPABASE_KEY, SUPABASE_URL
from app.utils.gerador_cutter import geradorCutter
import json

with open("app/utils/keywords.json", encoding='utf-8') as keywordsjson:
    keys = json.load(keywordsjson)
    

supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')

@aluno_bp.route('/dashboard')
def dashboard():
    if 'role' in session and session['role'] == 'aluno':
        
        response = supabase_client.table('pedidos').select("*").eq("id_aluno", f"{session['user_id']}").execute()
        
        # Carregar os pedidos do aluno
        pedidoUser = response.data[0]
        print(pedidoUser)
        return render_template('aluno/dashboard.html',pedidos = pedidoUser)
    flash('Acesso não autorizado.', 'danger')
    return redirect(url_for('auth.login'))

@aluno_bp.route('/cadastrar_pedido', methods=['GET', 'POST'])
def cadastrar_pedido():
    if request.method == 'POST':
        nomeAutor = request.form.get("nomeAutor")
        sobrenomeAutor = request.form.get("sobrenomeAutor")
        nomeCoautor = request.form.get("nomeCoautor")
        sobrenomeCoautor = request.form.get("sobrenomeCoautor")
        titulo = request.form.get("titulo")
        subtitulo = request.form.get("subtitulo")
        curso = request.form.get("curso")
        ano = request.form.get("ano")
        instituicao = request.form.get("instituicao")
        cidade = request.form.get("cidade")
        paginas = request.form.get("paginas")
        ilustracao = request.form.get("ilustracaoCheckbox")
        tabela = request.form.get("tabelaCheckbox")
        tamanho = request.form.get("tamanho")
        bibliografia = request.form.get("bibliografia")
        keywords =  request.form.get("keywords")
        cutter =  geradorCutter(sobrenomeAutor,titulo)
        cdd =  request.form.get("cdd")
        
        
        
        response = (supabase_client.table('pedidos').insert({
            "id_aluno": session['user_id'],
            "nome_autor": nomeAutor,
            "sobrenome_autor": sobrenomeAutor,
            "nome_coautor": nomeCoautor,
            "sobrenome_coautor": sobrenomeCoautor,
            "titulo": titulo,
            "sub_titulo": subtitulo,
            "curso": curso,
            "ano_publicacao": ano,
            "instituicao": instituicao,
            "cidade": cidade,
            "numero_pag": paginas,
            "ilustracao": ilustracao,
            "tabela": tabela,
            "tamanho": tamanho,
            "bibliografia": bibliografia,
            "palavras_chaves": keywords,
            "cod_cutter": cutter,
            "cdd": cdd
        }).execute())
        
        
        flash('Pedido cadastrado com sucesso!', 'success')
        return redirect(url_for('aluno.dashboard'))
    return render_template('aluno/cadastrar_pedido.html',keywords = keys )

@aluno_bp.route('/detalhes_pedido/<uuid:pedido_id>')
def detalhes_pedido(pedido_id):
    
    response = supabase_client.table('pedidos').select("*").eq("id", f"{pedido_id}").execute()
    pedidoUser = response.data[0]
    return render_template('aluno/detalhes.html', pedido_id=pedido_id, pedido = pedidoUser)

