from functools import wraps
from flask import request, jsonify, current_app
import jwt


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({"erro": "Token ausente!"}), 401
        
        token = auth.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithm=["HS256"]
            )



        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado!"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token invalido!"}), 401
        
        request.user_id = payload["sub"]

        return fn(*args, **kwargs)
    
    return wrapper