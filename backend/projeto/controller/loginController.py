from services.cadastroLogin.loginServices import LoginServices
from DTOs.loginDTO.loginResponseDTO import LoginResponseDTO
from auth.JWTServices import JWTServices
from repositories.querysCadastroLogin.agenteRepository import AgenteRepository
from repositories.querysCadastroLogin.atletaRepository import AtletaRepository



class LoginController:

    @staticmethod
    def autenticacao(dto):
        usuario = LoginServices.autenticacao_usuario(dto.email, dto.senha)

        if not usuario:
            return None
        
        if usuario.tipo_usuario == 'atleta':
            informacoes_adicionais = AtletaRepository.buscar_atleta_id_usuario(usuario.id)

        else:
            informacoes_adicionais = AgenteRepository.buscar_agente_usuario_id(usuario.id)
            
        token = JWTServices.gerar_token(usuario)

        return LoginResponseDTO(usuario, informacoes_adicionais, token)
    

        