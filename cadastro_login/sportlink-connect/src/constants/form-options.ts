export const ESTADOS_BRASIL = [
  { value: 'AC', label: 'Acre' },
  { value: 'AL', label: 'Alagoas' },
  { value: 'AP', label: 'Amapá' },
  { value: 'AM', label: 'Amazonas' },
  { value: 'BA', label: 'Bahia' },
  { value: 'CE', label: 'Ceará' },
  { value: 'DF', label: 'Distrito Federal' },
  { value: 'ES', label: 'Espírito Santo' },
  { value: 'GO', label: 'Goiás' },
  { value: 'MA', label: 'Maranhão' },
  { value: 'MT', label: 'Mato Grosso' },
  { value: 'MS', label: 'Mato Grosso do Sul' },
  { value: 'MG', label: 'Minas Gerais' },
  { value: 'PA', label: 'Pará' },
  { value: 'PB', label: 'Paraíba' },
  { value: 'PR', label: 'Paraná' },
  { value: 'PE', label: 'Pernambuco' },
  { value: 'PI', label: 'Piauí' },
  { value: 'RJ', label: 'Rio de Janeiro' },
  { value: 'RN', label: 'Rio Grande do Norte' },
  { value: 'RS', label: 'Rio Grande do Sul' },
  { value: 'RO', label: 'Rondônia' },
  { value: 'RR', label: 'Roraima' },
  { value: 'SC', label: 'Santa Catarina' },
  { value: 'SP', label: 'São Paulo' },
  { value: 'SE', label: 'Sergipe' },
  { value: 'TO', label: 'Tocantins' },
];



// ================ POSIÇÕES ============================= //
export const POSICOES_FUTEBOL = [
  { value: 'goleiro', label: 'Goleiro' },
  { value: 'lateral_direito', label: 'Lateral Direito' },
  { value: 'lateral_esquerdo', label: 'Lateral Esquerdo' },
  { value: 'zagueiro', label: 'Zagueiro' },
  { value: 'volante', label: 'Volante' },
  { value: 'meia', label: 'Meia' },
  { value: 'meia_atacante', label: 'Meia Atacante' },
  { value: 'ponta_direita', label: 'Ponta Direita' },
  { value: 'ponta_esquerda', label: 'Ponta Esquerda' },
  { value: 'centroavante', label: 'Centroavante' },
  { value: 'atacante', label: 'Atacante' },
];

export const POSICOES_FUTSAL = [
  { value: 'goleiro', label: 'Goleiro' },
  { value: 'fixo', label: 'Fixo' },
  { value: 'ala_direito', label: 'Ala Direito' },
  { value: 'ala_esquerdo', label: 'Ala Esquerdo' },
  { value: 'pivo', label: 'Pivô' },
];

export const POSICOES_BASQUETE = [
  { value: 'armador', label: 'Armador' },
  { value: 'ala_armador', label: 'Ala-Armador' },
  { value: 'ala', label: 'Ala' },
  { value: 'ala_pivo', label: 'Ala-Pivô' },
  { value: 'pivo', label: 'Pivô' },
];


export const POSICOES_VOLEI = [
  { value: 'levantador', label: 'Levantador' },
  { value: 'oposto', label: 'Oposto' },
  { value: 'ponteiro', label: 'Ponteiro' },
  { value: 'central', label: 'Central' },
  { value: 'libero', label: 'Líbero' },
];

export const ESPORTES = [
  { value: 'futebol', label: 'Futebol', posicoes: POSICOES_FUTEBOL },
  { value: 'futsal', label: 'Futsal', posicoes: POSICOES_FUTSAL },
  { value: 'basquete', label: 'Basquete', posicoes: POSICOES_BASQUETE },
  { value: 'volei', label: 'Vôlei', posicoes: POSICOES_VOLEI },
];
export const CATEGORIAS = [
  { value: 'sub7', label: 'Sub-7' },
  { value: 'sub9', label: 'Sub-9' },
  { value: 'sub11', label: 'Sub-11' },
  { value: 'sub13', label: 'Sub-13' },
  { value: 'sub15', label: 'Sub-15' },
  { value: 'sub17', label: 'Sub-17' },
  { value: 'sub20', label: 'Sub-20' },
  { value: 'sub23', label: 'Sub-23' },
  { value: 'profissional', label: 'Profissional' },
  { value: 'master', label: 'Master (+35)' },
];

export const PE_DOMINANTE = [
  { value: 'direito', label: 'Direito' },
  { value: 'esquerdo', label: 'Esquerdo' },
  { value: 'ambidestro', label: 'Ambidestro' },
];

export const MAO_DOMINANTE = [
  { value: 'direita', label: 'Direita' },
  { value: 'esquerda', label: 'Esquerda' },
  { value: 'ambidestro', label: 'Ambidestro' },
];

export const NIVEL_TECNICO = [
  { value: 'iniciante', label: 'Iniciante' },
  { value: 'intermediario', label: 'Intermediário' },
  { value: 'avancado', label: 'Avançado' },
  { value: 'profissional', label: 'Profissional' },
];

export const SITUACAO_ATLETA = [
  { value: 'base', label: 'Base / Formação' },
  { value: 'amador', label: 'Amador' },
  { value: 'profissional', label: 'Profissional' },
];

export const SEXO = [
  { value: 'masculino', label: 'Masculino' },
  { value: 'feminino', label: 'Feminino' },
  { value: 'outro', label: 'Outro / Prefiro não dizer' },
];

export const TIPO_PERFIL_AGENTE = [
  { value: 'empresario', label: 'Empresário' },
  { value: 'agente', label: 'Agente Esportivo' },
  { value: 'clube', label: 'Clube' },
  { value: 'escolinha', label: 'Escolinha / Academia' },
];

export const TIPO_DOCUMENTO = [
  { value: 'cpf', label: 'CPF' },
  { value: 'cnpj', label: 'CNPJ' },
];
