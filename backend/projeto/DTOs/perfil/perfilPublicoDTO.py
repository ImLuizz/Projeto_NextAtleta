class PerfilPublicoDTO:
    def __init__(self, usuario, atleta, perfil):
        self.usuario = usuario
        self.atleta = atleta
        self.perfil = perfil

    def build(self):
        return {
            "id": self.usuario.id,
            "nome": self.usuario.nome,
            "foto_perfil": self.usuario.foto_perfil,
            "cidade": self.atleta.cidade if self.atleta else None,
            "estado": self.atleta.estado if self.atleta else None,
            "esporte": self.perfil.esporte if self.perfil else None,
            "posicao": self.perfil.posicao if self.perfil else None,
            "categoria": self.perfil.categoria if self.perfil else None,
            "nivel_tecnico": self.perfil.nivel_tecnico if self.perfil else None,
        }
