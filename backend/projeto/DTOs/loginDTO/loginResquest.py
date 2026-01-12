class LoginRequestDTO:

    def __init__(self, form):

        if not form:
             raise ValueError("Dados do formulário ausentes!")
        
        self.email = form.get("email")
        self.senha = form.get("senha")

        self._validacao_campos()

     
    def _validacao_campos(self):
      
        if not self.email or self.email == '':
            raise ValueError("Campo do email ausente!")
        
        if not self.senha or self.senha == '':
            raise ValueError("Campo de senha ausente!")