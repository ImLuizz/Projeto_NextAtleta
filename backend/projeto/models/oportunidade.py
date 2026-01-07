from extension.extensao import db
from sqlalchemy import Enum
from sqlalchemy.sql import func

class Oportunidade(db.Model):
    """
    Representa uma oportunidade esportiva (Peneira, Testes) criada por uma entidade.
    
    Esta tabela centraliza todas as vagas disponíveis na plataforma. Ela não é vinculada diretamente
    ao Usuario, mas sim ao PerfilEsportivo (Clube/Empresário), garantindo que apenas perfis 
    profissionais possam criar oportunidades.

    Attributes:
        id (int): Identificador único da oportunidade.
        perfil_esportivo_id (int): FK do perfil (Clube/Agente) que publicou a vaga.
        tipo (Enum): Classificação do evento ('peneira', 'avaliacao', 'contrato', etc).
        status (Enum): Controle do ciclo de vida ('aberta', 'encerrada', etc).
    """
    __tablename__ = 'oportunidade'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # Vínculo com PerfilEsportivo (Clube, Agente, Escolinha)
    # ondelete='CASCADE': Se o clube for deletado, suas oportunidades somem.
    perfil_esportivo_id = db.Column(
        db.BigInteger,
        db.ForeignKey('perfil_esportivo.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment="ID do perfil profissional (Clube/Empresário) criador da vaga."
    )

    titulo = db.Column(db.String(150), nullable=False, comment="Título curto para exibição nos cards.")
    
    # Enums definem regras rígidas de negócio no banco
    tipo = db.Column(
        Enum('peneira', 'avaliacao', 'contrato', 'amistoso', 'concurso', name='tipo_oportunidade_enum'),
        nullable=False
    )

    # Segmentação da Oportunidade
    modalidade = db.Column(db.String(50), nullable=False, comment="Ex: Futebol, Vôlei, Basquete.")
    posicao_alvo = db.Column(db.String(50), comment="Ex: Goleiro. Se NULL, aceita todas as posições.")
    categoria_idade = db.Column(db.String(50), comment="Ex: Sub-17, 2008-2009.")
    
    genero_alvo = db.Column(
        Enum('masculino', 'feminino', 'misto', name='genero_oportunidade_enum'),
        default='misto'
    )

    # Localização
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    local_especifico = db.Column(db.String(255), comment="Nome do local, Estádio, CT ou Endereço.")

    # Datas Críticas
    data_evento = db.Column(db.DateTime, nullable=False, comment="Data e hora que a avaliação ocorrerá.")
    data_limite_inscricao = db.Column(db.DateTime, comment="Data limite para o botão de inscrição sumir.")

    # Detalhamento
    descricao = db.Column(db.Text, nullable=False, comment="Texto livre com detalhes completos.")
    requisitos = db.Column(db.Text, comment="Lista de exigências (ex: levar chuteira society, RG original).")

    # Controle Interno
    ativo = db.Column(db.Boolean, default=True, comment="Soft delete ou pausa manual da exibição.")
    
    status = db.Column(
        Enum('aberta', 'encerrada', 'cancelada', 'em_analise', name='status_oportunidade_enum'),
        default='aberta',
        nullable=False,
        comment="Estado atual do ciclo de vida da oportunidade."
    )

    # Auditoria
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamentos SQLAlchemy
    perfil_criador = db.relationship('PerfilEsportivo', backref='oportunidades_criadas')
    inscricoes = db.relationship('Inscricao', back_populates='oportunidade', cascade='all, delete-orphan')

    def to_dict(self):
        """
        Serializa o objeto para um dicionário Python (formato JSON-friendly).
        
        Útil para retornar dados em APIs REST sem expor diretamente o objeto SQLAlchemy.
        Inclui dados achatados (flattened) do perfil criador para facilitar o frontend.

        Returns:
            dict: Dicionário contendo os dados da oportunidade e resumo do criador.
        """
        return {
            "id": self.id,
            "perfil_esportivo_id": self.perfil_esportivo_id,
            "titulo": self.titulo,
            "tipo": self.tipo,
            "modalidade": self.modalidade,
            "posicao_alvo": self.posicao_alvo,
            "categoria_idade": self.categoria_idade,
            "cidade": self.cidade,
            "estado": self.estado,
            "data_evento": self.data_evento.isoformat() if self.data_evento else None,
            "status": self.status,
            "ativo": self.ativo,
            # Flattening: Trazendo dados do relacionamento para facilitar o frontend
            "nome_clube": self.perfil_criador.nome_publico if self.perfil_criador else None,
            "logo_clube": self.perfil_criador.logo if self.perfil_criador else None
        }