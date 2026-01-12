from models.perfilEsportivo import PerfilEsportivo

class AgenteRepository:

    @staticmethod
    def buscar_agente_usuario_id(id):
        agente = PerfilEsportivo.query.filter_by(usuario_id = id).first()

        return agente