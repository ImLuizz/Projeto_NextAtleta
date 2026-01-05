from models.atleta import Atleta
from extension.extensao import db

class AtletaRepository:

    @staticmethod
    def criar(atleta: Atleta):
        db.session.add(atleta)
        db.session.flush()
        return atleta
