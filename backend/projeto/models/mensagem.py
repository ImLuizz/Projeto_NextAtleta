from extension.extensao import db
from sqlalchemy.sql import func

class Mensagem(db.Model):
    __tablename__ = 'mensagem'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    conversa_id = db.Column(db.BigInteger, db.ForeignKey('conversa.id'), nullable=False)
    remetente_id = db.Column(db.BigInteger, db.ForeignKey('usuario.id'), nullable=False)
    
    conteudo = db.Column(db.Text, nullable=False)
    lida = db.Column(db.Boolean, nullable=False, default=False)
    
    created_at = db.Column(
        db.DateTime, 
        nullable=False, 
        server_default=func.now()
    )

    conversa = db.relationship('Conversa', back_populates='mensagens')
    remetente = db.relationship('Usuario')

    def to_dict(self):
        return {
            "id": self.id,
            "conversa_id": self.conversa_id,
            "remetente_id": self.remetente_id,
            "conteudo": self.conteudo,
            "lida": self.lida,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
