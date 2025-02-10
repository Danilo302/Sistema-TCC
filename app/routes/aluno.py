from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.config import supabase_client
from app.utils.gerador_cutter import geradorCutter
from app.routes.auth import aluno_required
import json

with open("app/utils/keywords.json", encoding='utf-8') as keywordsjson:
    keys = json.load(keywordsjson)
    



aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')


@aluno_bp.route('/dashboard')
@aluno_required
def dashboard():
    if 'role' in session and session['role'] == 'aluno':
        
        response = supabase_client.table('pedidos').select("*").eq("id_aluno", f"{session['user_id']}").execute()
        
        # Carregar os pedidos do aluno
        pedidoUser = response.data[0] if response.data else None
        
        return render_template('aluno/dashboard.html',pedidos = pedidoUser)
    flash('Acesso não autorizado.', 'danger')
    return redirect(url_for('auth.login'))

@aluno_bp.route('/cadastrar_pedido', methods=['GET', 'POST'])
@aluno_required
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
        ilustracao = request.form.get("ilustracao")
        tabela = request.form.get("tabela")
        tamanho = request.form.get("tamanho")
        bibliografia = request.form.get("bibliografia")
        keywords =  request.form.get("keywords")
        cutter =  geradorCutter(sobrenomeAutor,titulo)
        cdd =  request.form.get("cdd")
        semestre = request.form.get("semestre")
        data_defesa = request.form.get("data-defesa")
        horario = request.form.get("horario")
        turno = request.form.get("turno")
        orientador = request.form.get("orientador")
        tema_pesquisa = request.form.get("tema_pesquisa")
        atividades_desenvolvidas = request.form.get("atividades_desenvolvidas")
        contribuicoes_pesquisa = request.form.get("contribuicoes_pesquisa")
        membro1 = request.form.get("membro1")
        membro2 = request.form.get("membro2")
        
        
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
            "cdd": cdd,
            "semestre": semestre,
            "data_defesa": data_defesa,
            "horario": horario,
            "turno": turno,
            "orientador":orientador,
            "tema_pesquisa":tema_pesquisa,
            "atividades_desenvolvidas": atividades_desenvolvidas,
            "contribuicoes_pesquisa": contribuicoes_pesquisa,
            "membro1": membro1,
            "membro2": membro2
            
        }).execute())
        
        
        flash('Pedido cadastrado com sucesso!', 'success')
        return redirect(url_for('aluno.dashboard'))
    return render_template('aluno/cadastrar_pedido.html',keywords = keys )

@aluno_bp.route('/detalhes_pedido/<uuid:pedido_id>', methods=['GET', 'POST'])
@aluno_required
def detalhes_pedido(pedido_id):
    
    response = supabase_client.table('pedidos').select("*").eq("id", f"{pedido_id}").execute()
    pedidoUser = response.data[0]

    if request.method == 'POST':
        if 'delete' in request.form:  # Verifica se a ação é deletar
            if pedidoUser['status'] == 'pendente':  # Apenas pedidos pendentes podem ser deletados
                supabase_client.table('pedidos').delete().eq('id', pedido_id).execute()
                flash("Pedido deletado com sucesso!", "success")
                return redirect(url_for('aluno.dashboard'))
            else:
                flash("Apenas pedidos com status 'pendente' podem ser deletados.", "danger")
        else:  # Atualizar pedido
            if pedidoUser['status'] == 'pendente':
                # Obtém dados do formulário
                dados_atualizados = {
                    'titulo': request.form.get('titulo'),
                    'sub_titulo': request.form.get('sub_titulo'),
                    'curso': request.form.get('curso'),
                    'nome_autor': request.form.get('nome_autor'),
                    'sobrenome_autor': request.form.get('sobrenome_autor'),
                    'nome_coautor': request.form.get('nome_coautor'),
                    'sobrenome_coautor': request.form.get('sobrenome_coautor'),
                    'ano_publicacao': request.form.get('ano_publicacao'),
                    'instituicao': request.form.get('instituicao'),
                    'cidade': request.form.get('cidade'),
                    'numero_pag': request.form.get('numero_pag'),
                    'ilustracao': request.form.get('ilustracao'),
                    'tabela': request.form.get('tabela'),
                    'bibliografia': request.form.get('bibliografia'),
                    'palavras_chaves': request.form.get('palavras_chaves'),
                    'cod_cutter': geradorCutter(request.form.get('sobrenome_autor'), request.form.get('titulo')),
                    'cdd': request.form.get('cdd'),
                    'tamanho': request.form.get('tamanho'),
                }

                # Atualiza no banco
                supabase_client.table('pedidos').update(dados_atualizados).eq('id', pedido_id).execute()
                flash("Pedido atualizado com sucesso!", "success")
                return redirect(url_for('aluno.detalhes_pedido', pedido_id=pedido_id))
    return render_template('aluno/detalhes.html', pedido_id=pedido_id, pedido = pedidoUser, keywords = keys)
