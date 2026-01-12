
class LoginResponseDTO:

    def __init__(self, usuario, informacoes_adicionais, token):
        self.user = {
            "id": usuario.id,
            "nome": usuario.nome,
            "tipo": usuario.tipo_usuario,
            "maior_idade": informacoes_adicionais.maior_idade if informacoes_adicionais.maior_idade else None,
            "documento_validado": informacoes_adicionais.documento_validado,
            "possui_responsavel": informacoes_adicionais.possui_responsavel if informacoes_adicionais.possui_responsavel else None,
            "email_verificado": usuario.email_verificado

        }
        self.token = token
        
        
    def to_dict(self):
        print(self.user)
        return {
            "success": True,
            "user": self.user,
            "token": self.token
        }