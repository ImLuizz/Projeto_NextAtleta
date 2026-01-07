from .perfilPublicoDTO import PerfilPublicoDTO

class PerfilPrivadoDTO:
    def __init__(self, usuario, atleta, perfil):
        self.usuario = usuario
        self.atleta = atleta
        self.perfil = perfil

    def build(self):
        return {
            **PerfilPublicoDTO(self.usuario, self.atleta, self.perfil).build(),
            "email": self.usuario.email,
            "telefone": self.usuario.telefone,
            "cpf": self.atleta.cpf_numero if self.atleta else None,
            "data_nascimento": (
                self.atleta.data_nascimento.isoformat()
                if self.atleta and self.atleta.data_nascimento
                else None
            ),
            "maior_idade": self.atleta.maior_idade if self.atleta else None,
        }
