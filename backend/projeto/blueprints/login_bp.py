from flask import Blueprint, request, jsonify
from DTOs.loginDTO.loginResquest import LoginRequestDTO
from controller.loginController import LoginController


login_bp = Blueprint("login", __name__)


@login_bp.route('/', methods=['POST'])
def login():
    try:
        data = request.get_json(silent=True)
        dto = LoginRequestDTO(data)

        resultado = LoginController.autenticacao(dto)

        if not resultado:
            return jsonify({"message": "Email ou senha invalidos!"}), 401


        return jsonify(resultado.to_dict()), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

