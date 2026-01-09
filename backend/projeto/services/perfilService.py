from extension.extensao import db
from repositories.querysPerfil.queryPerfil import PerfilRepository
from DTOs.perfil.perfilPublicoDTO import PerfilPublicoDTO
from DTOs.perfil.perfilPrivadoDTO import PerfilPrivadoDTO
from DTOs.perfil.atualizacaoPerfilDTO import AtualizacaoPerfilDTO


class PerfilService:

    @staticmethod
    def get_perfil(usuario_id: int, visitante_id: int | None):
        usuario, atleta, perfil = PerfilRepository.buscar_por_usuario_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado")

        if visitante_id == usuario_id:
            DTO = PerfilPrivadoDTO(usuario, atleta, perfil)
        else:
            DTO = PerfilPublicoDTO(usuario, atleta, perfil)

        return DTO.build()

    @staticmethod
    def atualizar_perfil(usuario_id: int, dados: dict, solicitante_id: int):
        if usuario_id != solicitante_id:
            raise PermissionError("Você não pode editar este perfil")

        DTO = AtualizacaoPerfilDTO(dados)
        DTO.validar()

        usuario, atleta, perfil = PerfilRepository.buscar_por_usuario_id(usuario_id)

        if not atleta or not perfil:
            raise ValueError("Perfil incompleto")

        PerfilRepository.atualizar_atleta(atleta, DTO.dados_atleta)
        PerfilRepository.atualizar_perfil(perfil, DTO.dados_perfil)

        db.session.commit()
