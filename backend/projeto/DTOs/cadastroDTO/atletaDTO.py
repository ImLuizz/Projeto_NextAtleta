class CadastroAtletaDTO:

    def __init__(self, form_data: dict, files: dict):
        self.form_data = form_data
        self.files = files
        self.data_final = {}

    def validar(self):
        if not self.form_data:
            raise ValueError("Dados do formulário ausentes")

    def processar_documentos(self, tratamento_dados_service):
        arquivo_unico = self.files.get('arquivo_documento_unico')

        if arquivo_unico:
            info = tratamento_dados_service.extrair_dados(arquivo_unico)
            self._mapear_dados_documento(info)

        else:
            frente = self.files.get('arquivo_documento_frente')
            verso = self.files.get('arquivo_documento_verso')

            if not frente or not verso:
                raise ValueError("Envie frente e verso do documento")

            info_frente = tratamento_dados_service.extrair_dados(frente)
            info_verso = tratamento_dados_service.extrair_dados(verso)

            self._mapear_dados_documento({
                "nome": info_frente.get("nome"),
                "data_nascimento": info_frente.get("data_nascimento"),
                "rg": info_verso.get("rg"),
                "cpf": info_verso.get("cpf")
            })

    def _mapear_dados_documento(self, info: dict):
        self.data_final.update({
            "nome_documento": info.get("nome"),
            "data_nascimento_documento": info.get("data_nascimento"),
            "rg_documento": info.get("rg"),
            "cpf_documento": info.get("cpf")
        })

    def validar_cpf(self, tratamento_dados_service):
        cpf = self.data_final.get("cpf_documento")

        if not cpf:
            raise ValueError("CPF não encontrado no documento")

        if not tratamento_dados_service.validar_cpf(cpf):
            raise ValueError("CPF inválido")

    def build(self):
   
        return {
            **self.form_data,
            **self.data_final
        }
