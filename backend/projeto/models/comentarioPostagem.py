from extension.extensao import db
from sqlalchemy.sql import func

class ComentarioPostagem(db.Model):
    """
    Representa um comentário feito por um usuário em uma postagem.

    Cada comentário pertence a uma única postagem e a um único usuário.
    Comentários podem responder outros comentários dentro da mesma tabela.
    A tabela armazena o texto do comentário e informações de auditoria.
    """

    __tablename__ = 'comentario_postagem'

    # Identificador único do comentário
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # Conteúdo textual do comentário
    conteudo = db.Column(
        db.Text,
        nullable=False,
        comment="Texto do comentário."
    )

    # Postagem à qual o comentário pertence
    postagem_id = db.Column(
        db.BigInteger,
        db.ForeignKey('postagem.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment="ID da postagem comentada."
    )

    # Usuário que criou o comentário
    usuario_id = db.Column(
        db.BigInteger,
        db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment="ID do usuário autor do comentário."
    )

    # Comentário pai (se for uma resposta)
    comentario_pai_id = db.Column(
        db.BigInteger,
        db.ForeignKey('comentario_postagem.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True,
        comment="ID do comentário pai, se este for uma resposta."
    )

    # Indica se o comentário está ativo ou foi removido logicamente
    ativo = db.Column(
        db.Boolean,
        default=True,
        comment="Soft delete do comentário."
    )

    # Data e hora em que o comentário foi criado
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        comment="Data e hora da criação do comentário."
    )

    # Data e hora da última atualização do comentário
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relacionamento com a postagem
    postagem = db.relationship('Postagem', back_populates='comentarios')

    # Relacionamento com o usuário
    usuario = db.relationship('Usuario', backref='comentarios')

    # Relacionamento com comentários filhos (respostas)
    respostas = db.relationship('ComentarioPostagem',backref=db.backref('comentario_pai', 
    remote_side=[id]), cascade='all, delete-orphan')

    def to_dict(self):
        """
        Converte o objeto ComentarioPostagem em um dicionário Python.

        Essa conversão facilita o envio dos dados para o frontend,
        especialmente em respostas de APIs no formato JSON.
        """
        return {
            "id": self.id,
            "conteudo": self.conteudo,
            "postagem_id": self.postagem_id,
            "usuario_id": self.usuario_id,
            "comentario_pai_id": self.comentario_pai_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "ativo": self.ativo,
            "nome_usuario": self.usuario.nome if self.usuario else None,
            "foto_usuario": self.usuario.foto_perfil if self.usuario else None
        }