from models.usuario import Usuario
from models.atleta import Atleta
from models.perfilAtleta import PerfilAtleta
from extension.extensao import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from repositories.querysCadastroLogin.usuarioRepository import UsuarioRepository
from repositories.querysCadastroLogin.atletaRepository import AtletaRepository
from repositories.querysCadastroLogin.perfilAtletaRepository import PerfilAtletaRepository

from services.tratamento_dados import Tratamento_dados

class CadastroService:

    @staticmethod
    def cadastrar(dados):
        try:
            data_doc = dados['data_nascimento_documento']
            data_form = datetime.strptime(
                dados['data_nascimento'], "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

            if data_doc != data_form:
                raise ValueError("Datas não coincidem")

            maior_idade = Tratamento_dados.maior_idade(data_doc)

            senha_hash = generate_password_hash(dados['senha'])

            usuario = Usuario(
                nome=dados['nome'].title().strip(),
                email=dados['email'].strip().lower(),
                senha_hash=senha_hash,
                tipo_usuario='atleta',
                status='ativo'
            )

            UsuarioRepository.criar(usuario)

            atleta = Atleta(
                usuario_id=usuario.id,
                data_nascimento=datetime.strptime(
                    dados['data_nascimento'], "%Y-%m-%d"
                ).date(),
                maior_idade=maior_idade,
                cidade=dados['cidade'],
                estado=dados['estado'],
                sexo=dados['sexo'],
                disponivel=dados['disponivel_oportunidades']
            )

            AtletaRepository.criar(atleta)

            perfil = PerfilAtleta(
                atleta_id=atleta.id,
                esporte=dados['esporte'],
                posicao=dados['posicao'],
                bio=dados['bio']
            )

            PerfilAtletaRepository.criar(perfil)

            db.session.commit()
            return usuario

        except IntegrityError:
            db.session.rollback()
            raise ValueError("Email já cadastrado")

        except Exception:
            db.session.rollback()
            raise

