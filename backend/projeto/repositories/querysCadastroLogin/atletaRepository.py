from models.atleta import Atleta
from extension.extensao import db

class AtletaRepository:

    @staticmethod
    def criar(atleta: Atleta):
        db.session.add(atleta)
        db.session.flush()
        return atleta

    @staticmethod
    def buscar_atleta_id_usuario(id):
        atleta = Atleta.query.filter_by(usuario_id = id).first()
        return atleta