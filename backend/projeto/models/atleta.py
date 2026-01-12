from extension.extensao import db
from sqlalchemy import Enum


class Atleta(db.Model):
    __tablename__ = 'atleta'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    usuario_id = db.Column(
        db.BigInteger,
        db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        unique=True
    )

    data_nascimento = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(30), nullable=False)
    documento_validado = db.Column(db.Boolean, default=False)

    maior_idade = db.Column(db.Boolean)
    possui_responsavel = db.Column(db.Boolean)

    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))

    altura_cm = db.Column(db.SmallInteger)
    peso_kg = db.Column(db.Numeric(5, 2))

    sexo = db.Column(
        Enum('masculino', 'feminino', 'outro', name='sexo_enum')
    )

    disponivel = db.Column(db.Boolean, default=True)
    nivel_confiabilidade = db.Column(db.SmallInteger, default=0)

    usuario = db.relationship('Usuario', backref='atleta', uselist=False)
    perfil = db.relationship('PerfilAtleta', back_populates='atleta', uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "data_nascimento": self.data_nascimento.isoformat(),
            "cidade": self.cidade,
            "estado": self.estado,
            "altura_cm": self.altura_cm,
            "peso_kg": float(self.peso_kg) if self.peso_kg else None,
            "sexo": self.sexo,
            "disponivel": self.disponivel,
            "nivel_confiabilidade": self.nivel_confiabilidade
        }
