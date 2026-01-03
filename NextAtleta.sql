
CREATE TABLE usuario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,

    tipo_usuario ENUM(
        'atleta',
        'admin',
        'empresario',
        'agente',
        'clube',
        'escolinha'
    ) NOT NULL DEFAULT 'atleta',

    status ENUM('ativo', 'inativo', 'bloqueado') NOT NULL DEFAULT 'ativo',
    email_verificado BOOLEAN NOT NULL DEFAULT FALSE,

    telefone VARCHAR(20),
    foto_perfil VARCHAR(255),

    ultimo_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_usuario_email ON usuario(email);
CREATE INDEX idx_usuario_tipo ON usuario(tipo_usuario);
CREATE INDEX idx_usuario_status ON usuario(status);

-- =========================
-- TABELA: perfil_esportivo
-- =========================
CREATE TABLE perfil_esportivo (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT NOT NULL,

    tipo_perfil ENUM('empresario', 'agente', 'clube', 'escolinha') NOT NULL,
    nome_publico VARCHAR(150) NOT NULL,
    descricao TEXT,

    cidade VARCHAR(100),
    estado CHAR(2),
    site VARCHAR(255),
    telefone VARCHAR(20),
    email_contato VARCHAR(150),
    logo VARCHAR(255),

    documento_tipo ENUM('CPF', 'CNPJ'),
    documento_numero VARCHAR(30),
    documento_validado BOOLEAN DEFAULT FALSE,
    data_validacao TIMESTAMP NULL,

    verificado BOOLEAN DEFAULT FALSE,

    verificacao_nivel ENUM(
        'basica',
        'automatica',
        'manual',
        'completa'
    ) NOT NULL DEFAULT 'basica',

    fonte_verificacao ENUM(
        'ocr',
        'automatica',
        'humana'
    ) NOT NULL DEFAULT 'ocr',

    status_verificacao ENUM('pendente', 'aprovado', 'rejeitado') DEFAULT 'pendente',
    motivo_rejeicao TEXT,

    verificado_por VARCHAR(30),
    verificado_em TIMESTAMP,

    verificado_quando TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_perfil_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON DELETE CASCADE
);

-- =========================
-- TABELA: atleta
-- =========================
CREATE TABLE atleta (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT NOT NULL UNIQUE,

    cpf VARCHAR(30),

    data_nascimento DATE NOT NULL,
    maior_idade BOOLEAN,
    possui_responsavel BOOLEAN,

    cidade VARCHAR(100),
    estado CHAR(2),

    altura_cm SMALLINT,
    peso_kg DECIMAL(5,2),

    sexo ENUM('masculino', 'feminino', 'outro'),
    disponivel BOOLEAN DEFAULT TRUE,
    nivel_confiabilidade SMALLINT DEFAULT 0,

    CONSTRAINT fk_atleta_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- =========================
-- TABELA: perfil_atleta
-- =========================
CREATE TABLE perfil_atleta (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    atleta_id BIGINT NOT NULL,

    esporte VARCHAR(50) NOT NULL,
    posicao VARCHAR(50) NOT NULL,
    categoria VARCHAR(50),


    bio TEXT,

    pe_dominante ENUM('direita', 'esquerda', 'ambidestro'),    
    mao_dominante ENUM('direita', 'esquerda', 'ambidestro'),    

    nivel_tecnico ENUM('iniciante', 'intermediario', 'avancado'),
    situacao ENUM('base', 'amador', 'profissional'),
    ativo BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,

    CONSTRAINT fk_perfil_atleta
        FOREIGN KEY (atleta_id)
        REFERENCES atleta(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX idx_perfil_atleta_esporte ON perfil_atleta(esporte);
CREATE INDEX idx_perfil_atleta_posicao ON perfil_atleta(posicao);
CREATE INDEX idx_perfil_atleta_categoria ON perfil_atleta(categoria);

-- =========================
-- TABELA: experiencia_esportiva
-- =========================
CREATE TABLE experiencia_esportiva (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    perfil_atleta_id BIGINT NOT NULL,

    tipo_experiencia ENUM('clube', 'escolinha', 'competicao') NOT NULL,
    nome_entidade VARCHAR(150) NOT NULL,
    cargo_funcao VARCHAR(100),

    data_inicio DATE,
    data_fim DATE,
    em_andamento BOOLEAN DEFAULT FALSE,

    cidade VARCHAR(100),
    estado CHAR(2),

    descricao TEXT,
    ordem_exibicao SMALLINT DEFAULT 0,
    verificada BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,

    CONSTRAINT fk_experiencia_perfil
        FOREIGN KEY (perfil_atleta_id)
        REFERENCES perfil_atleta(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX idx_experiencia_perfil ON experiencia_esportiva(perfil_atleta_id);
CREATE INDEX idx_experiencia_tipo ON experiencia_esportiva(tipo_experiencia);
CREATE INDEX idx_experiencia_verificada ON experiencia_esportiva(verificada);

-- =========================
-- TABELA: conquista_atleta
-- =========================
CREATE TABLE conquista_atleta (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    perfil_atleta_id BIGINT NOT NULL,

    tipo ENUM(
        'titulo',
        'premiacao_individual',
        'convocacao',
        'destaque',
        'recorde'
    ) NOT NULL,

    titulo VARCHAR(150) NOT NULL,
    competicao VARCHAR(150),
    ano YEAR,

    clube_representado VARCHAR(150),
    nivel ENUM('municipal', 'estadual', 'nacional', 'internacional'),

    descricao TEXT,

    verificada BOOLEAN DEFAULT FALSE,
    fonte_verificacao VARCHAR(255),
    ordem_exibicao SMALLINT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,

    CONSTRAINT fk_conquista_perfil
        FOREIGN KEY (perfil_atleta_id)
        REFERENCES perfil_atleta(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX idx_conquista_perfil ON conquista_atleta(perfil_atleta_id);
CREATE INDEX idx_conquista_tipo ON conquista_atleta(tipo);
CREATE INDEX idx_conquista_verificada ON conquista_atleta(verificada);
