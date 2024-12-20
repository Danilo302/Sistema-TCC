from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import supabase
from app.config import SUPABASE_KEY, SUPABASE_URL
import json

with open("app/utils/keywords.json", encoding='utf-8') as keywordsjson:
    keys = json.load(keywordsjson)
    
with open("app/utils/cutter.json", encoding='utf-8') as cutter:
    codCutter = json.load(cutter)

supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')

@aluno_bp.route('/dashboard')
def dashboard():
    if 'role' in session and session['role'] == 'aluno':
        
        #response = supabase_client.table('pedidos').select()
        # Carregar os pedidos do aluno
        return render_template('aluno/dashboard.html')
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
        bibliografia = request.fotm.get("bibliografia")
        keywords =  request.form.get("keywords")
        cutter =  request.form.get("cutter")
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
    return render_template('aluno/cadastrar_pedido.html',keywords = keys,cod_cutter = codCutter )
