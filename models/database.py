from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy() # Instancia o objeto db, que será usado para definir os modelos e se conectar ao banco

class BoardGame(db.Model):
    __tablename__ = 'board_game' # Define explicitamente o nome da tabela no banco
    
    # Coluna de ID (chave primária, única para cada jogo)
    id = db.Column(db.Integer, primary_key=True) 
     # Relacionamento: um jogo pode ter várias imagens associadas
    imagens = db.relationship('Imagem', backref='boardgame', lazy=True)
     
    titulo = db.Column(db.String(150))
    ano = db.Column(db.Integer)
    idade = db.Column(db.String(150))
    designer = db.Column(db.String(150))
    artista = db.Column(db.String(150))
    editora = db.Column(db.String(150))
    dominio = db.Column(db.String(150))
    mecanica = db.Column(db.String(500))
    categoria = db.Column(db.String(150))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    
    def __init__(self, titulo, ano, idade, designer, artista,
                 editora, dominio, mecanica, categoria, preco, quantidade):
        self.titulo = titulo
        self.ano = ano
        self.idade = idade
        self.designer = designer
        self.artista = artista
        self.editora = editora
        self.dominio = dominio
        self.mecanica = mecanica
        self.categoria = categoria
        self.preco = preco
        self.quantidade = quantidade
        
        
class Imagem(db.Model):
    __tablename__ = 'imagem' # Nome da tabela no banco para armazenar imagens
    
    # Coluna ID da imagem (chave primária)
    id = db.Column(db.Integer, primary_key=True)
    # Tipo da imagem (ex: 'Capa', 'Contracapa', 'Tabuleiro', 'Peças')
    tipo = db.Column(db.String(100))
    # Caminho do arquivo da imagem (normalmente dentro da pasta static, ex: 'img/capas/jogo.jpg')
    caminho = db.Column(db.String(300))
    # Chave estrangeira: relaciona esta imagem com um jogo da tabela board_game
    boardgame_id = db.Column(db.Integer, db.ForeignKey('board_game.id'), nullable=False)
    
    def __init__(self, tipo, caminho, boardgame_id):
        self.tipo = tipo
        self.caminho = caminho
        self.boardgame_id = boardgame_id
    