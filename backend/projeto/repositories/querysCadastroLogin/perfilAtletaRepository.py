from models.perfilAtleta import PerfilAtleta
from extension.extensao import db

class PerfilAtletaRepository:

    @staticmethod
    def criar(perfil: PerfilAtleta):
        db.session.add(perfil)
        return perfil

