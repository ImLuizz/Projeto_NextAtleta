from models.usuario import Usuario
from models.atleta import Atleta
from models.perfilAtleta import PerfilAtleta
from models.perfilEsportivo import PerfilEsportivo
from extension.extensao import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import re
from datetime import datetime, timezone, date
from services.formador_mensagem import FormadorMensagem
from services.tratamento_dados import Tratamento_dados


class CadastroController:

   @staticmethod
   def cadastrar_usuario_com_atleta(dados):
       try:
           print(dados)
           data_nascimento_documento = dados['data_nascimento_documento']
           data_nascimento_digitado = datetime.strptime(dados['data_nascimento'], "%Y-%m-%d").strftime("%d/%m/%Y")

           if data_nascimento_documento != data_nascimento_digitado:
               print("Data de nascimento digitada e do documento não coincidem!")
               raise ValueError("Data de nascimento digitada e do documento não coincidem!")
           
           maior_idade = Tratamento_dados.maior_idade(data_nascimento_documento)
           possui_responsavel = not maior_idade
           print("maior idade: ", maior_idade)
               
           senha_hash = generate_password_hash(
               dados['senha'], method="pbkdf2:sha256", salt_length=16
           )
        
           usuario = Usuario(
               nome=dados['nome'].title().strip(),
               email=dados['email'].strip().lower(),
               senha_hash=senha_hash,
               tipo_usuario='atleta',
               status='ativo',
               email_verificado=False,
               telefone=dados.get('telefone'),
               foto_perfil=dados.get('foto_perfil')
           )
   
           db.session.add(usuario)
           db.session.flush()  
           
           data_nascimento = datetime.strptime(
               dados['data_nascimento'], "%Y-%m-%d"
           ).date()
   
           atleta = Atleta(
               usuario_id=usuario.id,
               data_nascimento=data_nascimento,
               cpf=dados['cpf_documento'], 
               maior_idade = maior_idade,
               possui_responsavel = possui_responsavel,
               cidade=dados['cidade'],
               estado=dados['estado'],
               altura_cm=dados['altura_cm'],
               peso_kg=dados['peso_kg'],
               sexo=dados['sexo'],
               disponivel=dados['disponivel_oportunidades'] == 'true',
               nivel_confiabilidade=1
           )
   
           db.session.add(atleta)
           db.session.flush()  
   
           perfil = PerfilAtleta(
               atleta_id=atleta.id,
               esporte=dados['esporte'],
               posicao=dados['posicao'],
               categoria=dados['categoria'],
               pe_dominante=dados['pe_dominante'],
               bio=dados['bio'],
               mao_dominante=dados['mao_dominante'],
               nivel_tecnico=dados['nivel_tecnico'],
               situacao=dados['situacao'],
               ativo=True
           )
   
           db.session.add(perfil)
           db.session.commit()
   
           return usuario
   
       except IntegrityError as e: # Captura erros de violação de contraints, como email duplicado ou violação de unique
           db.session.rollback()
           print(str(e))
           raise ValueError("Email já cadastrado")
   
       except KeyError as e: # Captura quando dados['campo'] não existe
           db.session.rollback()
           print(str(e))
           raise ValueError(f"Campo ausente: {e}")
   
       except Exception as e: # Captura erros inesperados
           db.session.rollback()
           print(str(e))
           raise ValueError("Erro interno ao cadastrar atleta")
       
   @staticmethod
   def cadastro_usuario_com_agente(dados):
       try:
           documento_form = re.sub(r"\D", "", dados['numero_documento'])
           documento_img = re.sub(r"\D", "", dados['cpf_documento'])

           if documento_form != documento_img:
               return {
                   "sucess": False,
                   "message": f"O numero do {dados['tipo_documento']} digitado e o da imagem enviada são diferentes!"
               }
               
           print(dados)
           senha_hash = generate_password_hash(
               dados['senha'], method="pbkdf2:sha256", salt_length=16
           )
   
           usuario = Usuario(
               nome=dados['nome'].title().strip(),
               email=dados['email'].strip().lower(),
               senha_hash=senha_hash,
               tipo_usuario=dados['tipo_usuario'],
               status='ativo',
               email_verificado=False,
               telefone=dados['telefone'],
               foto_perfil=dados['foto_perfil']
           )
   
           db.session.add(usuario)
           db.session.flush() 


           novo_agente = PerfilEsportivo(
               usuario_id = usuario.id,
               tipo_perfil = dados['tipo_usuario'],
               nome_publico = dados['nome_publico'],
               descricao = dados['descricao'],
               cidade = dados['cidade'],
               estado = dados['estado'],
               site = dados['site'],
               telefone = dados['telefone_contato'],
               email_contato = dados['email_contato'],
               logo = None,
               documento_tipo = dados['tipo_documento'].upper(),
               documento_numero = dados['numero_documento'],
               documento_validado = False,
               data_validacao = None,
               status_verificacao = 'pendente',
               motivo_rejeicao = "Fase de teste ainda",
               verificado_em = datetime.now(timezone.utc)

           )

           db.session.add(novo_agente)
           db.session.commit()

           return {
                   "sucess": False,
                   "user": usuario.to_dict(),
                   "message": FormadorMensagem.formar_texto_cadastro_agente(novo_agente.status_verificacao)
               }

       except IntegrityError as e: # Captura erros de violação de contraints, como email duplicado ou violação de unique
           db.session.rollback()
           print(str(e))
           raise ValueError("Email já cadastrado")
   
       except KeyError as e: # Captura quando dados['campo'] não existe
           db.session.rollback()
           print(str(e))
           raise ValueError(f"Campo ausente: {e}")
   
       except Exception as e: # Captura erros inesperados
           db.session.rollback()
           print(str(e))
           raise ValueError("Erro interno ao cadastrar agente")
   