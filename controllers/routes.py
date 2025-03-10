import os
import urllib
import json
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename



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
            return redirect(url_for('boardgames'))

        return render_template('cadboardgames.html', boardgamelist=boardgamelist)
    
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