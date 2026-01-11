from extension.extensao import db
from sqlalchemy.sql import func

class Conversa(db.Model):
    __tablename__ = 'conversa'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    participante1_id = db.Column(db.BigInteger, db.ForeignKey('usuario.id'), nullable=False)
    participante2_id = db.Column(db.BigInteger, db.ForeignKey('usuario.id'), nullable=False)
    
    created_at = db.Column(
        db.DateTime, 
        nullable=False, 
        server_default=func.now()
    )
    
    updated_at = db.Column(
        db.DateTime, 
        nullable=False, 
        server_default=func.now(),
        onupdate=func.now()
    )

    participante1 = db.relationship('Usuario', foreign_keys=[participante1_id])
    participante2 = db.relationship('Usuario', foreign_keys=[participante2_id])
    
    mensagens = db.relationship('Mensagem', back_populates='conversa', lazy='dynamic') # Using dynamic to filter easily

    def to_dict(self):
        return {
            "id": self.id,
            "participante1": self.participante1.to_dict(),
            "participante2": self.participante2.to_dict(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
