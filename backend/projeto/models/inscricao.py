from extension.extensao import db
from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.sql import func

class Inscricao(db.Model):
    """
    Registra o interesse de um Atleta em uma Oportunidade específica.
    
    Funciona como uma tabela associativa (Many-to-Many) com atributos adicionais
    de controle de status e feedback.

    Restrições:
        Possui uma UniqueConstraint ('oportunidade_id', 'atleta_id') para impedir
        que o mesmo atleta se inscreva duas vezes na mesma oportunidade.

    Attributes:
        status (Enum): Define se o atleta foi aceito para teste, rejeitado, etc.
        feedback_clube (Text): Campo para o avaliador justificar a decisão.
    """
    __tablename__ = 'inscricao'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # Chaves Estrangeiras
    oportunidade_id = db.Column(
        db.BigInteger,
        db.ForeignKey('oportunidade.id', ondelete='CASCADE'),
        nullable=False
    )

    atleta_id = db.Column(
        db.BigInteger,
        db.ForeignKey('atleta.id', ondelete='CASCADE'),
        nullable=False
    )

    # Controle de Fluxo
    status = db.Column(
        Enum(
            'pendente',       # Inscrito, aguardando análise
            'aprovado',       # Aprovado na triagem inicial (vai para o campo)
            'rejeitado',      # Não passou na triagem online
            'lista_espera',   # Vagas acabaram, mas pode ser chamado
            'compareceu',     # Check-in realizado no dia do evento
            name='status_inscricao_enum'
        ),
        default='pendente',
        nullable=False
    )

    # Comunicação
    observacao_atleta = db.Column(db.String(255), comment="Msg curta do atleta ao se inscrever.")
    feedback_clube = db.Column(db.Text, comment="Feedback técnico ou motivo de rejeição enviado pelo clube.")

    # Auditoria
    created_at = db.Column(db.DateTime, server_default=func.now(), comment="Data da inscrição.")
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    oportunidade = db.relationship('Oportunidade', back_populates='inscricoes')
    atleta = db.relationship('Atleta', backref='inscricoes')

    # REGRA DE INTEGRIDADE DE DADOS
    __table_args__ = (
        UniqueConstraint('oportunidade_id', 'atleta_id', name='uq_atleta_oportunidade'),
    )

    def to_dict(self):
        """
        Serializa a inscrição.
        
        Returns:
            dict: Dados da inscrição e nome do atleta para listagens rápidas.
        """
        return {
            "id": self.id,
            "oportunidade_id": self.oportunidade_id,
            "atleta_id": self.atleta_id,
            "status": self.status,
            "data_inscricao": self.created_at.isoformat(),
            # Traz o nome do usuário associado ao atleta para evitar N+1 queries no front básico
            "atleta_nome": self.atleta.usuario.nome if (self.atleta and self.atleta.usuario) else None
        }