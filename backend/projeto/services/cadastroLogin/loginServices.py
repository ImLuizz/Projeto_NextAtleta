from repositories.querysCadastroLogin.usuarioRepository import UsuarioRepository
from werkzeug.security import check_password_hash


query = UsuarioRepository()

class LoginServices:

    @staticmethod
    def autenticacao_usuario(email, senha):
        usuario = query.buscar_por_email(email)

        if not usuario:
            return False

        if not check_password_hash(usuario.senha_hash, senha):
            return False
        
        return usuario
        

        

