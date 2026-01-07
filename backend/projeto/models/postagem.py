from extension.extensao import db
from sqlalchemy.sql import func

class Postagem(db.Model):
    """
    Representa uma postagem criada por um usuário na plataforma.

    A tabela de postagens armazena conteúdos publicados no feed,
    permitindo imagens e vídeos, com uma legenda opcional.
    Cada postagem pertence a um único usuário.
    """

    __tablename__ = 'postagem'

    # Identificador único da postagem
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # Arquivo de mídia da postagem (imagem ou vídeo)
    conteudo = db.Column(
        db.String(255),
        nullable=False,
        comment="Caminho ou URL do arquivo de mídia."
    )

    # Texto opcional que acompanha a postagem
    legenda = db.Column(
        db.Text,
        nullable=True,
        comment="Legenda opcional da postagem."
    )

    # Usuário responsável pela criação da postagem
    usuario_id = db.Column(
        db.BigInteger,
        db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment="ID do usuário que criou a postagem."
    )

    # Indica se a postagem está ativa ou foi removida logicamente
    ativo = db.Column(
        db.Boolean,
        default=True,
        comment="Soft delete da postagem."
    )

    # Data e hora em que a postagem foi criada
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        comment="Data e hora da publicação."
    )

    # Data e hora da última atualização da postagem
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relacionamento com o usuário criador da postagem
    usuario = db.relationship('Usuario', backref='postagens')

    # Comentários associados à postagem
    comentarios = db.relationship('ComentarioPostagem', back_populates='postagem', cascade='all, delete-orphan')

    # Curtidas associadas à postagem
    curtidas = db.relationship('Curtida', backref='postagem')

    def to_dict(self):
        """
        Converte o objeto Postagem em um dicionário Python.

        Essa conversão facilita o envio dos dados para o frontend,
        principalmente em respostas de APIs no formato JSON.
        """
        return {
            "id": self.id,
            "conteudo": self.conteudo,
            "legenda": self.legenda,
            "usuario_id": self.usuario_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "ativo": self.ativo,
            "nome_usuario": self.usuario.nome if self.usuario else None,
            "foto_usuario": self.usuario.foto if self.usuario else None,
            "quantidade_curtidas": len(self.curtidas)
        }