from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from classes import db, Usuario, Categoria, Produto, Tamanho
from flask_paginate import Pagination, get_page_args
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

rotas_app = Blueprint('rotas_app', __name__, template_folder='templates', static_folder='static')

PRODUTOS_POR_PAGINA = 4

@rotas_app.route('/templates/backend/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates/backend', filename)

@rotas_app.route('/new')
def new():
    usuarios = Usuario.query.all()
    return render_template('cadastrar.html', usuarios=usuarios)


@rotas_app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('rotas_app.index'))

@rotas_app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('login.html', usuarios=usuarios)

# Rota dashboard (protegida por login)
@rotas_app.route('/dashboard')
@login_required
def dashboard():
    total_usuarios = Usuario.query.count()
    total_categorias = Categoria.query.count()
    total_produtos = Produto.query.count()
    return render_template('home.html', usuario=current_user, total_usuarios=total_usuarios, total_categorias=total_categorias, total_produtos=total_produtos)


# Rota de login
@rotas_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email, senha=senha).first()

        if usuario:
            login_user(usuario)
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('rotas_app.dashboard'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')

    return render_template('login.html')

# Rota de logout
@rotas_app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('rotas_app.index'))

#rotas produtos
@rotas_app.route('/listaprodutos')
@login_required
def produtos():
    # Configurando a paginação
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Defina o número desejado de itens por página

    # Obtendo a lista de produtos paginada
    produtos_paginados = Produto.query.filter_by(usuario=current_user).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('produto/listaprodutos.html', produtos_paginados=produtos_paginados)

@rotas_app.route('/new_produto')
@login_required
def new_produto():
    categorias = Categoria.query.filter_by(usuario=current_user)
    return render_template('produto/cadastrar_produto.html', categorias=categorias)

# Adicione esta rota para excluir uma categoria
@rotas_app.route('/delete_produto/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def delete_produto(produto_id):
    # Obtém a categoria pelo ID
    produto = Produto.query.get(produto_id)

    # Verifica se a categoria existe
    if produto:
        # Remove a categoria do banco de dados
        db.session.delete(produto)
        db.session.commit()

        flash('Produto excluída com sucesso.', 'success')  # Mensagem de sucesso
    else:
        flash('Produto não encontrada.', 'error')  # Mensagem de erro

    return redirect(url_for('rotas_app.produtos'))

@rotas_app.route('/cadastrar_produto', methods=['POST'])
@login_required
def cadastrar_produto():
    nome = request.form['nome']
    preco = request.form['preco']
    descricao = request.form['descricao']
    categoria_id = request.form['categoria']  # Obtém a categoria selecionada

    # Obtém a categoria pelo ID
    categoria = Categoria.query.get(categoria_id)
    usuario = current_user

    if categoria:
        novo_produto = Produto(nome=nome, preco=preco, descricao=descricao, categoria=categoria, usuario=usuario)
        db.session.add(novo_produto)
        db.session.commit()

        flash('Produto cadastrado com sucesso.', 'success')
    else:
        flash('Categoria não encontrada.', 'error')

    return redirect(url_for('rotas_app.produtos'))


# Adicione esta rota para excluir uma categoria
@rotas_app.route('/delete_categoria/<int:categoria_id>', methods=['GET', 'POST'])
@login_required
def delete_categoria(categoria_id):
    # Obtém a categoria pelo ID
    categoria = Categoria.query.get(categoria_id)

    # Verifica se a categoria existe
    if categoria:
        # Remove a categoria do banco de dados
        db.session.delete(categoria)
        db.session.commit()

        flash('Categoria excluída com sucesso.', 'success')  # Mensagem de sucesso
    else:
        flash('Categoria não encontrada.', 'error')  # Mensagem de erro

    return redirect(url_for('rotas_app.categorias'))


# Suas rotas categoria existentes
@rotas_app.route('/listacategoria')
@login_required
def categorias():
    categorias = Categoria.query.filter_by(usuario=current_user).all()
    return render_template('categoria/listaCategoria.html', categorias=categorias)

@rotas_app.route('/new_categoria')
@login_required
def new_categoria():
    return render_template('categoria/cadastrar_categoria.html')

@rotas_app.route('/cadastrar_categoria', methods=['GET', 'POST'])
@login_required
def cadastrar_categoria():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']

        # Verificar se a categoria já existe pelo nome e descrição
        categoria_existente = Categoria.query.filter_by(nome=nome, descricao=descricao).first()

        if categoria_existente:
            flash('Categoria já existe.', 'error')  # Mensagem de erro
            return render_template('categoria/cadastrar_categoria.html')

        # Se não existir, criar a nova categoria
        novo_categoria = Categoria(nome=nome, descricao=descricao, usuario=current_user)
        db.session.add(novo_categoria)
        db.session.commit()

        flash('Categoria cadastrada com sucesso.', 'success')  # Mensagem de sucesso

        return redirect(url_for('rotas_app.categorias'))

    # Tratar o método GET aqui (se necessário)
    return render_template('categoria/cadastrar_categoria.html')

@rotas_app.route('/contar_usuarios')
def contar_usuarios():
    total_usuarios = Usuario.query.count()
    return render_template('statistic.html', total_usuarios=total_usuarios)

# Rota dashboard (protegida por login)
@rotas_app.route('/admin/dashboard')
@login_required
def admin():
    total_usuarios = Usuario.query.count()
    total_categorias = Categoria.query.count()
    total_produtos = Produto.query.count()
    return render_template('backend/dashboard.html', usuario=current_user)

#Tamanho e quantidade
@rotas_app.route('/listatamanho')
@login_required
def tamanhos():
    # Configurando a paginação
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Defina o número desejado de itens por página

    # Obtendo a lista de produtos paginada
    tamanhos_paginados = Tamanho.query.filter_by(usuario=current_user).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('tamanho/listatamanho.html', tamanhos_paginados=tamanhos_paginados)

@rotas_app.route('/new_tamanho')
@login_required
def new_tamanho():
    produtos = Produto.query.filter_by(usuario=current_user)
    return render_template('tamanho/cadastrar_tamanho.html', produtos=produtos)

@rotas_app.route('/cadastrar_tamanho', methods=['POST'])
@login_required
def cadastrar_tamanho():
    tamanho = request.form['tamanho']
    quantidade = request.form['quantidade']
    produto_id = request.form['produto']  # Obtém a categoria selecionada

    # Obtém a categoria pelo ID
    produto = Produto.query.get(produto_id)
    usuario = current_user

    if produto:
        novo_produto = Tamanho(produto=produto, usuario=usuario, quantidade=quantidade,tamanho=tamanho)
        db.session.add(novo_produto)
        db.session.commit()

        flash('Tamanho cadastrado com sucesso.', 'success')
    else:
        flash('Produto não encontrado.', 'error')

    return redirect(url_for('rotas_app.tamanhos'))




#
#
# selects da loja e produtos
@rotas_app.route('/dashboard')
@login_required
def listar_produtos():
    # Obtendo a lista de todos os produtos ordenados por categoria
    todos_produtos = Produto.query.order_by(Produto.categoria_id).all()

    # Agrupando os produtos por categoria usando um dicionário
    produtos_por_categoria = {}
    for produto in todos_produtos:
        categoria_id = produto.categoria_id
        produtos_por_categoria.setdefault(categoria_id, []).append(produto)

    # Ordenando as categorias por ID
    categorias_ordenadas = sorted(produtos_por_categoria.keys())

    # Obtendo a lista final de produtos ordenados por categoria
    produtos_ordenados = [produto for categoria_id in categorias_ordenadas for produto in produtos_por_categoria[categoria_id]]

    return render_template('loja/home.html', produtos=produtos_ordenados)
