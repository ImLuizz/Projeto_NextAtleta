from datetime import datetime, timezone
from flask import current_app
import jwt

class JWTServices:

    @staticmethod
    def gerar_token(usuario):
        expires = datetime.now(timezone.utc) + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]

        payload = {
            "sub": usuario.id,
            "tipo": usuario.tipo_usuario,
            
            "exp": expires,
            "iat": datetime.now(timezone.utc)
        }

        return jwt.encode(
            payload,
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256"
        )


