from models.conversa import Conversa
from models.mensagem import Mensagem
from extension.extensao import db
from sqlalchemy import or_, and_, desc

class MessageService:
    
    @staticmethod
    def get_or_create_conversation(user_id1, user_id2):
        if user_id1 == user_id2:
            raise ValueError("Users must be different")

        # Checa se a conversa existe
        conversa = Conversa.query.filter(
            or_(
                and_(Conversa.participante1_id == user_id1, Conversa.participante2_id == user_id2),
                and_(Conversa.participante1_id == user_id2, Conversa.participante2_id == user_id1)
            )
        ).first()

        if conversa:
            return conversa

        # Cria uma nova conversa se ela não existir
        new_conversa = Conversa(
            participante1_id=user_id1,
            participante2_id=user_id2
        )
        db.session.add(new_conversa)
        db.session.commit()
        
        return new_conversa

    @staticmethod
    def send_message(conversa_id, remetente_id, conteudo):
        if not conteudo:
            raise ValueError("Content cannot be empty")

        conversa = Conversa.query.get(conversa_id)
        if not conversa:
            raise ValueError("Conversation not found")

        if conversa.participante1_id != remetente_id and conversa.participante2_id != remetente_id:
            raise PermissionError("User is not a participant in this conversation")

        new_message = Mensagem(
            conversa_id=conversa_id,
            remetente_id=remetente_id,
            conteudo=conteudo
        )
        
        db.session.add(new_message)
        
        # Atualiza o timestamp da conversa
        conversa.updated_at = func.now()
        
        db.session.commit()
        return new_message

    @staticmethod
    def list_conversations(user_id):
        conversas = Conversa.query.filter(
            or_(Conversa.participante1_id == user_id, Conversa.participante2_id == user_id)
        ).order_by(desc(Conversa.updated_at)).all()
        
        result = []
        for conversa in conversas:
            last_message = conversa.mensagens.order_by(desc(Mensagem.created_at)).first()
            other_user = conversa.participante2 if conversa.participante1_id == user_id else conversa.participante1
            
            result.append({
                "conversa": conversa.to_dict(),
                "last_message": last_message.to_dict() if last_message else None,
                "other_user": other_user.to_dict()
            })
            
        return result

    @staticmethod
    def list_messages(conversa_id, user_id, page=1, per_page=20):
        conversa = Conversa.query.get(conversa_id)
        if not conversa:
            raise ValueError("Conversation not found")
            
        if conversa.participante1_id != user_id and conversa.participante2_id != user_id:
            raise PermissionError("User is not a participant")

        pagination = conversa.mensagens.order_by(desc(Mensagem.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            "messages": [msg.to_dict() for msg in pagination.items][::-1], # Return chronological order
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }

    @staticmethod
    def mark_messages_as_read(conversa_id, user_id):
        conversa = Conversa.query.get(conversa_id)
        if not conversa:
            raise ValueError("Conversation not found")

        if conversa.participante1_id != user_id and conversa.participante2_id != user_id:
            raise PermissionError("User is not a participant")

        # Marca as mensagens enviadas pelo OUTRO usuário como lidas
        other_user_id = conversa.participante2_id if conversa.participante1_id == user_id else conversa.participante1_id
        
        unread_messages = Mensagem.query.filter(
            Mensagem.conversa_id == conversa_id,
            Mensagem.remetente_id == other_user_id,
            Mensagem.lida == False
        ).all()
        
        for msg in unread_messages:
            msg.lida = True
            
        db.session.commit()
        return len(unread_messages)
