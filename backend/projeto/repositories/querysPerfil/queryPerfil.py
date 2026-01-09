from models import Usuario, Atleta, PerfilAtleta
from extension.extensao import db

class PerfilRepository:

    @staticmethod
    def buscar_por_usuario_id(usuario_id: int):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return None, None, None 

        atleta = Atleta.query.filter_by(usuario_id=usuario.id).first()
        perfil = None

        if atleta:
            perfil = PerfilAtleta.query.filter_by(atleta_id=atleta.id).first()

        return usuario, atleta, perfil

    @staticmethod
    def atualizar_atleta(atleta, dados: dict):
        for campo, valor in dados.items():
            if hasattr(atleta, campo):
                setattr(atleta, campo, valor)

    @staticmethod
    def atualizar_perfil(perfil, dados: dict):
        for campo, valor in dados.items():
            if hasattr(perfil, campo):
                setattr(perfil, campo, valor)
