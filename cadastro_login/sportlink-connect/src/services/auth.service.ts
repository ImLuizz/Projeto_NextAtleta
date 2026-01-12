import type {
  LoginData,
  AuthResponse,
  AthleteRegistrationData,
  AgentRegistrationData,
  Usuario,
  PerfilAtleta,
  PerfilEsportivo,
  DocumentoVerificacao,
} from '@/types/auth.types';

const API_BASE_URL = 'http://127.0.0.1:5000';

// Helper for API calls
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const defaultHeaders: HeadersInit = {}
  
  if(!(options.body instanceof FormData)){
      defaultHeaders['Content-Type'] = 'application/json';
  }
 
  const token = localStorage.getItem('auth_token');
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Erro de conexão' }));
    throw new Error(error.message || 'Erro na requisição');
  }

  return response.json();
}

// Upload file helper
async function uploadFile(file: File, folder: string): Promise<string> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('folder', folder);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
    headers: {
      Authorization: `Bearer ${localStorage.getItem('auth_token') || ''}`,
    },
  });

  if (!response.ok) {
    throw new Error('Erro ao fazer upload do arquivo');
  }

  const data = await response.json();
  return data.url;
}

// Auth Service
export const authService = {
  // Login
  async login(data: LoginData): Promise<AuthResponse> {
    try {
      const response = await apiCall<AuthResponse>('/login/', {
        method: 'POST',
        body: JSON.stringify(data),
      });

      if (response.success && response.data?.token) {
        localStorage.setItem('auth_token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }

      return response;
    } catch (error) {
      return {
        success: false,
        message: 'Erro ao fazer login',
        error: error instanceof Error ? error.message : 'Erro desconhecido',
      };
    }
  },

  // Logout
  async logout(): Promise<void> {
    try {
      await apiCall('/auth/logout', { method: 'POST' });
    } finally {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
    }
  },

  // Register Athlete
  async registerAthlete(data: AthleteRegistrationData): Promise<AuthResponse> {
    try {
      
      const formData = new FormData();

      // ======================
      // Dados do usuário
      // ======================
      formData.append('nome', data.nome);
      formData.append('email', data.email);
      formData.append('senha', data.senha);
      formData.append('telefone', data.telefone);

      // Arquivo
      if (data.foto_perfil) {
        formData.append('foto_perfil', data.foto_perfil);
      }

      // ======================
      // Dados do atleta
      // ======================
      formData.append('data_nascimento', data.data_nascimento);
      formData.append('cidade', data.cidade);
      formData.append('estado', data.estado);
      formData.append('altura_cm', String(data.altura_cm));
      formData.append('peso_kg', String(data.peso_kg));
      formData.append('sexo', data.sexo);
      formData.append(
        'disponivel_oportunidades',
        String(data.disponivel_oportunidades)
      );

      // Arquivo
      if (data.arquivo_documento_unico) {
        formData.append('arquivo_documento_unico', data.arquivo_documento_unico);
      }
      if (data.arquivo_documento_frente) {
        formData.append('arquivo_documento_frente', data.arquivo_documento_frente);
      }
      if (data.arquivo_documento_verso) {
        formData.append('arquivo_documento_verso', data.arquivo_documento_verso);
      }

      // ======================
      // Dados do perfil atleta
      // ======================
      formData.append('esporte', data.esporte);
      formData.append('posicao', data.posicao);
      formData.append('categoria', data.categoria);
      formData.append('pe_dominante', data.pe_dominante);
      formData.append('mao_dominante', data.mao_dominante);
      formData.append('nivel_tecnico', data.nivel_tecnico);
      formData.append('situacao', data.situacao);
      formData.append('bio', data.bio ?? '');


      const userResponse = await apiCall<{ user: Usuario }>('/cadastrar/atleta', {
        method: 'POST',
        body: formData,
      });

     
      return {
        success: true,
        message: 'Cadastro realizado com sucesso!',
        data: {
          user: userResponse.user,
          token: '',
        },
      };
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Erro desconhecido',
        error: error instanceof Error ? error.message : 'Erro desconhecido',
      };
    }
  },

  // Register Agent
  async registerAgent(data: AgentRegistrationData): Promise<AuthResponse> {
    try {
      const formData = new FormData();

    // dados do usuário
    formData.append('nome', data.nome);
    formData.append('email', data.email);
    formData.append('senha', data.senha);
    formData.append('telefone', data.telefone);
    formData.append('tipo_usuario', data.tipo_perfil);

    // dados do perfil esportivo
    formData.append('nome_publico', data.nome_publico);
    formData.append('descricao', data.descricao);
    formData.append('cidade', data.cidade);
    formData.append('estado', data.estado);
    formData.append('site', data.site ?? '');
    formData.append('telefone_contato', data.telefone_contato);
    formData.append('email_contato', data.email_contato);

    // dados do documento
    formData.append('tipo_documento', data.tipo_documento);
    formData.append('numero_documento', data.numero_documento);

    // arquivos
    if (data.foto_perfil) {
      formData.append('foto_perfil', data.foto_perfil);
    }
    if (data.logo) {
      formData.append('logo', data.logo);
    }
    if (data.arquivo_documento) {
      formData.append('arquivo_documento', data.arquivo_documento);
    }

    const response = await apiCall<AuthResponse>('/cadastrar/agente', {
      method: 'POST',
      body: formData, 
    });

    

      return {
        success: true,
        message: 'Cadastro realizado! Seu perfil passará por validação.',
        data: {
          user: response.data!.user,
          token: '',
        },
      };
    } catch (error) {
      return {
        success: false,
        message: 'Erro ao realizar cadastro',
        error: error instanceof Error ? error.message : 'Erro desconhecido',
      };
    }
  },

  // Password reset request
  async requestPasswordReset(email: string): Promise<{ success: boolean; message: string }> {
    try {
      await apiCall('/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email }),
      });

      return {
        success: true,
        message: 'Email de recuperação enviado com sucesso',
      };
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Erro ao enviar email',
      };
    }
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  },

  // Get current user
  getCurrentUser(): Usuario | null {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  // Verify email
  async verifyEmail(token: string): Promise<{ success: boolean; message: string }> {
    try {
      await apiCall('/auth/verify-email', {
        method: 'POST',
        body: JSON.stringify({ token }),
      });

      return {
        success: true,
        message: 'Email verificado com sucesso',
      };
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Erro ao verificar email',
      };
    }
  },
};

export default authService;
