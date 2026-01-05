from flask import jsonify, request, Blueprint
from controller.cadastroController import CadastroController
from services.preProcessador_img import Preprocessador_img
from services.ocrService import OCRservices
from services.rg_parser import RGparse
from services.tratamento_dados import Tratamento_dados
from DTOs.cadastroDTO.atletaDTO import CadastroAtletaDTO
from DTOs.cadastroDTO.agenteDTO import CadastroAgenteDTO

cadastro_bp = Blueprint("cadastro", __name__)
controller = CadastroController()


@cadastro_bp.route('/', methods=['POST'])
def cadastrar_atleta ():
    try:
       dto = CadastroAtletaDTO(
           form_data=request.form.to_dict(),
           files= request.files
       )
       dto.validar()
       dto.processar_documentos(Tratamento_dados)
       dto.validar_cpf()

       data = dto.build()
        
       usuario = controller.cadastrar_usuario_com_atleta(data)

       return jsonify({
           "sucess": True,
           "user": usuario.to_dict()
       }), 500

    except ValueError as e:
        print(str(e))
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 400
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "success": False,
            "error": "Erro interno no servidor"
        }), 500

@cadastro_bp.route('/agente', methods=['POST'])
def cadastro_agente():
    try: 
        dto = CadastroAgenteDTO(
            form_data = request.form.to_dict(),
            files = request.files
        )

        dto.validar()
        dto.processar_documentos(Tratamento_dados)
        dto.validar_cpf()
        dados = dto.build()
 
        print("dados: ",dados, "\n")
        usuario = controller.cadastro_usuario_com_agente(dados)
        
        return jsonify(usuario), 200

        
    except ValueError as e:
        print(str(e))
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 400
    
    except Exception as e:
        print(e)
        return jsonify({
            "success": False,
            "error": "Erro interno no servidor"
        }), 500


