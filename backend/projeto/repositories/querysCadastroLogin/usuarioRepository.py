from models.usuario import Usuario
from extension.extensao import db
class UsuarioRepository:

    @staticmethod
    def criar(usuario: Usuario):
        db.session.add(usuario)
        db.session.flush()
        return usuario
