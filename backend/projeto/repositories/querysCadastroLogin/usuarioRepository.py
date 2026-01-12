from models.usuario import Usuario
from extension.extensao import db

class UsuarioRepository:

    @staticmethod
    def criar(usuario: Usuario):
        db.session.add(usuario)
        db.session.flush()
        return usuario
    
    @staticmethod
    def buscar_por_email(email):
        usuario = Usuario.query.filter_by(email = email).first()
        return usuario

