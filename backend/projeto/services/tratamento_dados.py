import re
from datetime import datetime, date
from services.preProcessador_img import Preprocessador_img
from services.ocrService import OCRservices
from services.rg_parser import RGparse


class Tratamento_dados:

    @staticmethod
    def valida_campos_funcao_interna(resposta):
        campos_invalidos = sum(
                1 for campo in ['rg', 'cpf', 'data_nascimento', 'nome']
                if resposta.get(campo) is None
            )

        if campos_invalidos < 2:
            return True
        
        else:
            return False

    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        try:
            if cpf is None:
                raise ValueError("CPF não informado")

            if not isinstance(cpf, str):
                raise TypeError("CPF deve ser uma string")

            # Remove tudo que não for número
            cpf_numerico = re.sub(r"\D", "", cpf)

            # Deve ter exatamente 11 dígitos
            if len(cpf_numerico) != 11:
                return False

            # Rejeita CPFs com todos os dígitos iguais
            if cpf_numerico == cpf_numerico[0] * 11:
                return False

            # Primeiro dígito verificador
            soma = 0
            for i in range(9):
                soma += int(cpf_numerico[i]) * (10 - i)

            resto = soma % 11
            dv1 = 0 if resto < 2 else 11 - resto

            if dv1 != int(cpf_numerico[9]):
                return False

            # Segundo dígito verificador
            soma = 0
            for i in range(10):
                soma += int(cpf_numerico[i]) * (11 - i)

            resto = soma % 11
            dv2 = 0 if resto < 2 else 11 - resto

            if dv2 != int(cpf_numerico[10]):
                return False

            return True

        except (ValueError, TypeError):
            
            return False

        except Exception as e:
            
            raise RuntimeError(f"Erro inesperado ao validar CPF: {e}")
        
    @staticmethod
    def maior_idade(data: str) -> bool:
        try:
            if not data:
                return False
            
            data_nascimento = datetime.strptime(data, "%d/%m/%Y").date()
            hoje = date.today()
            dia_nascimento = data_nascimento.day
            if data_nascimento.day == 29 and data_nascimento.month == 2:
                dia_nascimento = 28
       
            data_maioridade = date(
                data_nascimento.year + 18,
                data_nascimento.month,
                dia_nascimento
            )

            return hoje >= data_maioridade

        except ValueError:
            return False
        
    @staticmethod
    def extrair_dados(arquivo):
            imagem = Preprocessador_img.open_img(arquivo)
            text = OCRservices.extracao_text(imagem)
            resposta = RGparse(text).parse()
            print("resposta 1: ", resposta)
            
            deu_certo = Tratamento_dados.valida_campos_funcao_interna(resposta)

            if deu_certo:
                return resposta

            imagem_proc = Preprocessador_img.preprocess(imagem)
            text_proc = OCRservices.extracao_text(imagem_proc)
            resposta_proc = RGparse(text_proc).parse()
            print("resposta 2: ", resposta_proc)

            return resposta_proc
    

    
