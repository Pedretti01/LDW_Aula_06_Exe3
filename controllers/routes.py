from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.database import db, BoardGame, Imagem
import os
import uuid



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


   # Definindo tipos de arquivos permitidos
    FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
    def arquivos_permitidos(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES
    
    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        # Paginação - Definindo a variável page
        page = request.args.get('page', 1, type=int)
        
        # Obtendo todas as imagens paginadas do banco
        imagens = Imagem.query.paginate(page=page, per_page=8)
        
        # Verificando se a requisição é POST (upload de imagem)
        if request.method == 'POST':
            file = request.files['file']
            if not arquivos_permitidos(file.filename):
                flash("Utilize os tipos de arquivos referentes a imagem.", 'danger')
                return redirect(request.url)

            # Define o caminho para salvar as imagens da galeria
            filename = str(uuid.uuid4())  # Gerando um nome único para o arquivo
            caminho_imagem_galeria = os.path.join('static/galeria_img', filename)

            # Verifica se o diretório existe, se não, cria
            if not os.path.exists('static/galeria_img'):
                os.makedirs('static/galeria_img')  # Criação do diretório para galeria

            # Salva a imagem no diretório
            file.save(caminho_imagem_galeria)
            caminho_imagem = 'galeria_img/' + filename  # Caminho relativo no banco

            # Você pode ajustar o boardgame_id conforme necessário, ou fazer de forma dinâmica
            boardgame_id = 1  # Exemplo de id fixo ou pode ser variável

            # Criação da imagem no banco de dados
            img = Imagem(tipo="Capa", caminho=caminho_imagem, boardgame_id=boardgame_id)
            db.session.add(img)
            db.session.commit()

            flash("Imagem enviada com sucesso!", 'success')

        # Retorna a página de galeria com as imagens paginadas
        return render_template('galeria.html', imagens=imagens)