from flask import Blueprint
from controller.perfilController import PerfilController

perfil_bp = Blueprint(
    "perfil",
    __name__,
    url_prefix="/perfil"
)

perfil_bp.add_url_rule(
    "/<int:usuario_id>",
    view_func=PerfilController.get_perfil,
    methods=["GET"]
)

perfil_bp.add_url_rule(
    "/<int:usuario_id>",
    view_func=PerfilController.atualizar_perfil,
    methods=["PUT"]
)

