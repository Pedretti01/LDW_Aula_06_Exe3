from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from models.database import db, BoardGame, Imagem
import os
import urllib
import json


interessados_em_comprar = []

boardgamelist = [{'Titulo' : 'Tiny Epic Dungeons',
                'Ano' : 2021,
                'Idade' : 14,
                'Designer' : 'Scott Almes',
                'Artista' : 'Nikoletta Vaszi, Ian Rosenthaler, Benjamin Shulman',
                'Editora' : 'MeepleBR Jogos, Gamelyn Games',
                'Dominio' : 'Jogo Expert',
                'Mecanica' : 'Colocação de Peças, Cooperativo, Jogadores com Diferentes Habilidades, Rolagem de Dados, Tabuleiro Modular, Minijogo no Final, Preparação Variável, Solo/Grupo',
                'Categoria' : 'Miniaturas, Dungeon Crawler',
                'imagem_jogo' : 'images/Tiny_Epic_Dungeons.jpg'}]

def init_app(app):
    # Definir o diretório para salvar as imagens
    app.config['UPLOAD_FOLDER'] = 'static/images'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    # Função para verificar se a extensão do arquivo é permitida
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
    
    # Rota Principal
    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/boardgames', methods=['GET', 'POST'])
    def boardgames():
        
        boardgame = boardgamelist[0]
        
        if request.method =='POST':
            if request.form.get('interessado'):
                interessados_em_comprar.append(request.form.get('interessado'))
        
        return render_template('boardgames.html',
                                boardgame=boardgame,
                                interessados_em_comprar=interessados_em_comprar)
     
    
    # Rota Cadastro    
    @app.route('/cadboardgames', methods=['GET', 'POST'])
    def cadboardgames():
        if request.method == 'POST':
            # Obter os dados do Formulário
            titulo = request.form['titulo']
            ano = request.form['ano']
            idade = request.form['idade']
            designer = request.form['designer']
            artista = request.form['artista']
            editora = request.form['editora']
            dominio = request.form['dominio']
            mecanica = request.form['mecanica']
            categoria = request.form['categoria']
            
            
        # Verificar se a imagem foi carregada
        imagem_jogo = None
        if 'imagem_jogo' in request.files:
            file = request.files['imagem_jogo']
            if file and allowed_file(file.filename):
                # Verificar se o nome do arquivo não está vazio
                    if file.filename == '':
                        return 'Nenhuma imagem selecionada!', 400  # Retorna erro se o nome do arquivo estiver vazio
                    
                    # Gerar um nome seguro para o arquivo
                    filename = secure_filename(file.filename)
                    # Caminho completo para salvar o arquivo
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    # Verificar se o diretório existe e criá-lo se não existir
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])  # Criação do diretório
                    
                    # Salvar o arquivo
                    file.save(filepath)
                    imagem_jogo = 'images/' + filename  # Caminho relativo da imagem

            # Criar o novo boardgame
            new_boardgame = {
                'Titulo' : titulo,
                'Ano' : ano,
                'Idade' : idade,
                'Designer' : designer,
                'Artista' : artista,
                'Editora' : editora,
                'Dominio' : dominio,
                'Mecanica' : mecanica,
                'Categoria' : categoria,
                'imagem_jogo' : imagem_jogo  # Caminho da imagem
            }        

            # Adicionar à lista de jogos
            boardgamelist.append(new_boardgame)  # Corrigido aqui para adicionar o novo jogo corretamente
            
            # Redirecionar para a página de Board Games após o cadastro
            return redirect(url_for('mostrar_boardgames'))

        return render_template('cadboardgames.html', boardgamelist=boardgamelist)
    
    
    # Rota Consumo de API
    @app.route('/apiboardgames', methods=['GET', 'POST'])
    @app.route('/apiboardgames/<int:id>', methods=['GET', 'POST'])
    def apiboardgames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        data = res.read()
        boardgamesjson = json.loads(data)  # Aqui você carrega os dados da API
        if id:
            binfo = None
            for b in boardgamesjson:
                if b.get('id') == id:  # Corrigir a sintaxe para acessar a chave do dicionário
                    binfo = b  # Se encontrar a id, armazene o boardgame
                    break
            if binfo:
                return render_template('boardgameinfo.html', binfo=binfo)
            else:
                return f'Boardgame com a ID {id} não foi encontrado.', 404  # Adicionando um retorno adequado caso não encontre
        else:
            return render_template('apiboardgames.html', boardgamesjson=boardgamesjson)
        
    # Função para verificar se o arquivo tem uma extensão permitida
    def allowed_file(filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
        
    #Rota Estoque
    @app.route('/estoque', methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        if id:
            # Selecionando o cadastro no banco para ser excluído
            boardgame = BoardGame.query.get(id)
            # Deleta o cadastro pela ID
            db.session.delete(boardgame)
            db.session.commit()
            return redirect(url_for('estoque'))
        
        
        # Cadastra um novo produto
        if request.method == 'POST':
            newboardgame = BoardGame(request.form['titulo'], int(request.form['ano']), request.form['idade'],
                                     request.form['designer'], request.form['artista'], request.form['editora'],
                                     request.form['dominio'], request.form['mecanica'], request.form['categoria'],
                                     float(request.form['preco']), int(request.form['quantidade']))
            
            # Primeiro salva o cadastro no banco para gerar o ID
            db.session.add(newboardgame)
            db.session.commit()

            # Upload da imagem — use .get() para evitar erro 400
            imagem_jogo = request.files.get('imagem_jogo')
            if imagem_jogo and imagem_jogo.filename != '':
                if '.' in imagem_jogo.filename and imagem_jogo.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
                    filename = secure_filename(imagem_jogo.filename)
                    filepath = os.path.join('static/images', filename)

                    if not os.path.exists('static/images'):
                        os.makedirs('static/images')

                    imagem_jogo.save(filepath)
                    caminho_imagem = 'images/' + filename

                    # Agora o ID existe
                    nova_imagem = Imagem(tipo="Capa", caminho=caminho_imagem, boardgame_id=newboardgame.id)
                    # Envia os valores para o banco
                    db.session.add(nova_imagem)
                    db.session.commit()

            return redirect(url_for('estoque'))

        else:
            # Paginação
            # A variável abaixo captura o valor de page que foi passado pelo metodo GET.
            # E define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de Registros por página (Definido 5)
            per_page = 5
            # abaixo está sendo feito um SELECT no banco a partir da página informada (page)
            # e filtrando os registros de 5 em 5 (per_page)
            boardgames_page = BoardGame.query.paginate(page=page, per_page=per_page)
            return render_template('estoque.html', boardgamesestoque=boardgames_page)
            
            # Metodo do SQLAlchemy que faz um select geral no banco na tabela BoardGames
            #boardgamesestoque = BoardGame.query.all()
            #return render_template('estoque.html', boardgamesestoque=boardgamesestoque)
    
    
    
    # Rota de Edição    
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        b = BoardGame.query.get(id)
        # Editando os cadastros com as informações do formulário
        if request.method == 'POST':
            b.titulo = request.form['titulo']
            b.ano = request.form['ano']
            b.idade = request.form['idade']
            b.designer = request.form['designer']
            b.artista = request.form['titulo']
            b.editora = request.form['editora']
            b.dominio = request.form['deminio']
            b.mecanica = request.form['mecanica']
            b.categoria = request.form['categoria']
            b.preco = request.form['preco']
            b.quantidade = request.form['quantidade']
            
            # Upload da nova imagem (opcional)
        imagem_nova = request.files.get('imagem_jogo')
        if imagem_nova and imagem_nova.filename != '':
            if '.' in imagem_nova.filename and imagem_nova.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
                filename = secure_filename(imagem_nova.filename)
                filepath = os.path.join('static/images', filename)

                if not os.path.exists('static/images'):
                    os.makedirs('static/images')

                imagem_nova.save(filepath)
                caminho_imagem = 'images/' + filename

                # Atualiza a imagem do tipo "Capa" (ou adiciona nova se não existir)
                imagem_existente = next((img for img in b.imagens if img.tipo == "Capa"), None)
                if imagem_existente:
                    imagem_existente.caminho = caminho_imagem
                else:
                    nova_imagem = Imagem(tipo="Capa", caminho=caminho_imagem, boardgame_id=b.id)
                    db.session.add(nova_imagem)
                       
            db.session.commit()
            return redirect(url_for('estoque'))
             
        return render_template('editboardgame.html', b=b)