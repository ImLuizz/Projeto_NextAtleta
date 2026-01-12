from extension.extensao import db
from sqlalchemy import Enum, Integer, Boolean, String
from sqlalchemy.sql import func


class PerfilAtleta(db.Model):
    __tablename__ = 'perfil_atleta'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    atleta_id = db.Column(
        db.BigInteger,
        db.ForeignKey('atleta.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )

    esporte = db.Column(db.String(50), nullable=False)
    posicao = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50))

    pe_dominante = db.Column(
        Enum('direito', 'esquerdo', 'ambidestro', name='pe_dominante_enum')
    )

    bio = db.Column(db.Text)

    mao_dominante= db.Column(
        Enum('direita', 'esquerda', 'ambidestro', name='mao_dominante_enum')
    )

    nivel_tecnico = db.Column(
        Enum('iniciante', 'intermediario', 'avancado', name='nivel_tecnico_enum')
    )

    situacao = db.Column(
        Enum('base', 'amador', 'profissional', name='situacao_enum')
    )

    ativo = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    deleted_at = db.Column(db.DateTime)

    atleta = db.relationship('Atleta', back_populates='perfil')
    experiencias = db.relationship(
        'ExperienciaEsportiva',
        back_populates='perfil_atleta',
        cascade='all, delete-orphan'
    )
    conquistas = db.relationship(
        'ConquistaAtleta',
        back_populates='perfil_atleta',
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "atleta_id": self.atleta_id,
            "esporte": self.esporte,
            "posicao": self.posicao,
            "categoria": self.categoria,
            "pe_dominante": self.pe_dominante,
            "bio": self.bio,
            "numero_camisa": self.numero_camisa,
            "nivel_tecnico": self.nivel_tecnico,
            "situacao": self.situacao,
            "ativo": self.ativo
        }
