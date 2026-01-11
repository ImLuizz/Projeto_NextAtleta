from flask import Blueprint, request, jsonify
from services.mensageria.message_service import MessageService

mensageria_bp = Blueprint('mensageria', __name__, url_prefix='/direct')


@mensageria_bp.route('/conversations', methods=['POST'])
def get_or_create_conversation():
    try:
        data = request.get_json()
        participante_id = data.get('participante_id')
        
        if not participante_id:
            return jsonify({'error': 'participante_id is required'}), 400

        conversa = MessageService.get_or_create_conversation(current_user.id, participante_id)
        return jsonify(conversa.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mensageria_bp.route('/conversations/<int:conversa_id>/messages', methods=['POST'])
def send_message(conversa_id):
    try:
        data = request.get_json()
        conteudo = data.get('conteudo')
        
        if not conteudo:
            return jsonify({'error': 'conteudo is required'}), 400

        mensagem = MessageService.send_message(conversa_id, current_user.id, conteudo)
        return jsonify(mensagem.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mensageria_bp.route('/conversations', methods=['GET'])
def list_conversations():
    try:
        conversas = MessageService.list_conversations(current_user.id)
        return jsonify(conversas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mensageria_bp.route('/conversations/<int:conversa_id>/messages', methods=['GET'])
def list_messages(conversa_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = MessageService.list_messages(conversa_id, current_user.id, page, per_page)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mensageria_bp.route('/conversations/<int:conversa_id>/read', methods=['PUT'])
def mark_messages_as_read(conversa_id):
    try:
        count = MessageService.mark_messages_as_read(conversa_id, current_user.id)
        return jsonify({'message': 'Messages marked as read', 'count': count}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500
