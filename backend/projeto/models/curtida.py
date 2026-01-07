from extension.extensao import db
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint

class Curtida(db.Model):
    """
    Representa uma curtida feita por um usuário.

    A curtida pode estar associada a uma postagem ou a um comentário.
    Um usuário pode curtir um item apenas uma vez.
    """

    __tablename__ = 'curtida'

    # Garante que um usuário não curta o mesmo item mais de uma vez
    __table_args__ = (
        UniqueConstraint('usuario_id', 'postagem_id', name='uq_usuario_postagem'),
        UniqueConstraint('usuario_id', 'comentario_id', name='uq_usuario_comentario'),
    )

    # Identificador único da curtida
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # Postagem curtida (quando a curtida for em uma postagem)
    postagem_id = db.Column(
        db.BigInteger,
        db.ForeignKey('postagem.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True,
        comment="ID da postagem curtida."
    )

    # Comentário curtido (quando a curtida for em um comentário ou resposta)
    comentario_id = db.Column(
        db.BigInteger,
        db.ForeignKey('comentario_postagem.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True,
        comment="ID do comentário curtido."
    )

    # Usuário que realizou a curtida
    usuario_id = db.Column(
        db.BigInteger,
        db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment="ID do usuário que realizou a curtida."
    )

    # Indica se a curtida está ativa
    ativo = db.Column(
        db.Boolean,
        default=True,
        comment="Soft delete da curtida."
    )

    # Data e hora em que a curtida foi criada
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        comment="Data e hora da curtida."
    )

    # Data e hora da última atualização da curtida
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relacionamento com a postagem
    postagem = db.relationship('Postagem', backref='curtidas')

    # Relacionamento com o comentário
    comentario = db.relationship('ComentarioPostagem', backref='curtidas')

    # Relacionamento com o usuário
    usuario = db.relationship('Usuario', backref='curtidas')

    def to_dict(self):
        """
        Converte o objeto Curtida em um dicionário Python.

        Essa conversão facilita o envio dos dados para o frontend,
        especialmente em respostas de APIs no formato JSON.
        """
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "postagem_id": self.postagem_id,
            "comentario_id": self.comentario_id,
            "ativo": self.ativo,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "nome_usuario": self.usuario.nome if self.usuario else None
        }