class AtualizacaoPerfilDTO:

    CAMPOS_ATLETA = {
        "cidade", "estado", "altura_cm", "peso_kg"
    }

    CAMPOS_PERFIL = {
        "bio", "posicao", "categoria", "nivel_tecnico"
    }

    def __init__(self, data: dict):
        self.dados_atleta = {
            k: v for k, v in data.items() if k in self.CAMPOS_ATLETA
        }
        self.dados_perfil = {
            k: v for k, v in data.items() if k in self.CAMPOS_PERFIL
        }

    def validar(self):
        if not self.dados_atleta and not self.dados_perfil:
            raise ValueError("Nenhum dado válido para atualização")
