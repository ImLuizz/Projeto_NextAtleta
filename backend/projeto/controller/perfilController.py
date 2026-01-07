from flask import jsonify, request
from services.perfilService import PerfilService
# Imagino que irão usar Flask Login, JWT ou algo parecido, então esse código só passa a efetivamente funcionar quando current_user e login_required forem devidamente implementados
from flask_login import current_user, login_required 


class PerfilController:
    @staticmethod
    def get_perfil(usuario_id):

        try:
            visitante_id = current_user.id

        except Exception as e:
            visitante_id = 0


        perfil = PerfilService.get_perfil(usuario_id, visitante_id)
        return jsonify(perfil), 200

    @staticmethod
    @login_required
    def atualizar_perfil(usuario_id):
        dados = request.get_json() or {}

        PerfilService.atualizar_perfil(
            usuario_id=usuario_id,
            dados=dados,
            solicitante_id=current_user.id
        )

        return jsonify({"message": "Perfil atualizado com sucesso"}), 200
