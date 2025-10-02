from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from .services import get_client, obtain_token, refresh_token, get_user_profile
import httpx


def _get_tokens(session):
    """
    Retorna os tokens de acesso e refresh da sessão.
    """
    return session.get('access'), session.get('refresh')


def _save_tokens(session, access: str, refresh: str | None = None):
    """
    Salva os tokens de acesso e refresh na sessão.
    """
    session['access'] = access
    if refresh:
        session['refresh'] = refresh


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Renderiza a página de login e processa o formulário de login.
    ### GET
    Renderiza o formulário de login.
    ### POST
    Processa o formulário de login, obtém os tokens e redireciona para a página inicial.

    ### Mensagens de Erro
    - "Email e senha são obrigatórios." se os campos estiverem vazios.
    - "Email ou senha incorretos, tente novamente." se as credenciais forem inválidas.
    - "Login falhou: {status_code} - {response_text}" para outros erros HTTP.
    - "Erro inesperado ao tentar logar: {error_message}" para exceções gerais
    """
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # Validação básica dos campos
        if not email or not password:
            messages.error(request, "Email e senha são obrigatórios.")
            return render(request, 'login.html')

        try:
            tokens = obtain_token(email, password)
            _save_tokens(request.session, tokens['access'], tokens['refresh'])
            messages.success(request, "Login realizado com sucesso!")
            return redirect('index')

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                messages.error(
                    request, "Email ou senha incorretos, tente novamente.")
            else:
                messages.error(
                    request, f"Login falhou: {e.response.status_code} - {e.response.text}")

        except Exception as e:  # Captura exceções gerais
            print(f"[DEBUG - Frontend - Login] Erro inesperado: {e}")
            messages.error(request, f"Erro inesperado ao tentar logar: {e}")
    return render(request, 'login.html')


def logout_view(request):
    """
    Realiza o logout do usuário, limpando a sessão e redirecionando para a página de login.
    """
    request.session.flush()
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('login')


def home_view(request):
    """
    Renderiza a página inicial, verificando o tipo de usuário autenticado.


    ### GET    
    Renderiza a página inicial com base no tipo de usuário.
    Em caso de falha na autenticação, redireciona para a página de login.

    ### Retorna
    - HttpResponse: Página inicial renderizada ou redirecionamento para login.

    ### Exceções
    - httpx.HTTPStatusError: Em caso de falha ao obter o perfil do usuário

    ### Mensagens de Erro
    - "Erro ao obter perfil do usuário: {status_code} - {response_text}"
    - "Erro inesperado ao obter perfil do usuário: {error_message}"
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    return render(request, 'index.html', {'user_type': user_type})


def cursos_list_view(request):
    """
    Renderiza a lista de cursos, verificando o tipo de usuário autenticado.

    ### GET
    Renderiza a página de cursos com a lista de cursos obtida da API.

    ### Mensagens de Erro
    - "Você não tem permissão para acessar os cursos." se o usuário não tiver permissão.
    - "Erro ao obter perfil do usuário: {status_code} - {response_text}"
    - "Erro inesperado ao obter perfil do usuário: {error_message}"
    - "Erro ao carregar cursos: {status_code} - {response_text}"
    - "Erro inesperado ao carregar cursos: {error_message}"
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    with get_client(access) as api:
        r = api.get('/cursos/')
        if r.status_code == 401 and refresh:
            try:
                new_tokens = refresh_token(refresh)
                _save_tokens(request.session, new_tokens.get(
                    'access'))
                r = get_client(new_tokens.get('access')).get('/cursos/')
                # Refresh user profile after token refresh
                user_profile = get_user_profile(new_tokens.get('access'))
                user_type = user_profile.get('tipo')
            except Exception:
                request.session.flush()
                return redirect('login')
        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                messages.error(
                    request, "Você não tem permissão para acessar os cursos.")
                request.session.flush()
                return redirect('login')
            raise
        cursos = r.json()

    return render(request, 'cursos.html', {'cursos': cursos, 'API_BASE_URL': settings.API_BASE_URL, 'user_type': user_type})


def perfis_list_view(request):
    """
    Renderiza a lista de perfis, verificando o tipo de usuário autenticado.

    ### GET 
    Renderiza a página de perfis com a lista de perfis obtida da API.

    ### Mensagens de Erro
    - "Você não tem permissão para acessar esta página." se o usuário não for do tipo 'Gerente'.
    - "Erro ao obter perfil do usuário: {status_code} - {response_text}"
    - "Erro inesperado ao obter perfil do usuário: {error_message}"
    - "Erro ao carregar perfis: {status_code} - {response_text}"
    - "Erro inesperado ao carregar perfis: {error_message}"
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    if user_type != 'Gerente':
        messages.error(
            request, "Você não tem permissão para acessar esta página.")
        return redirect('index')

    with get_client(access) as api:
        try:
            # Assumindo endpoint /perfis/
            perfis_response = api.get('/perfis/')
            perfis_response.raise_for_status()
            perfis = perfis_response.json()
        except httpx.HTTPStatusError as e:
            messages.error(
                request, f"Erro ao carregar perfis: {e.response.status_code} - {e.response.text}")
            request.session.flush()
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Erro inesperado ao carregar perfis: {e}")
            request.session.flush()
            return redirect('login')

    return render(request, 'perfis.html', {'perfis': perfis, 'API_BASE_URL': settings.API_BASE_URL, 'user_type': user_type})


@require_http_methods(["GET", "POST"])
def curso_detail_view(request, pk):
    """
    Renderiza os detalhes de um curso específico, incluindo a lista de disciplinas associadas.
    Permite adicionar novas disciplinas ao curso.

    ### GET
    Renderiza a página de detalhes do curso com a lista de disciplinas.

    ### POST
    Processa o formulário para adicionar uma nova disciplina ao curso.

    ### Mensagens de Erro
    - "Você precisa estar logado para ver os detalhes do curso." se o usuário não estiver autenticado.
    - "Erro ao obter perfil do usuário: {status_code} - {response_text}"
    - "Erro inesperado ao obter perfil do usuário: {error_message}"
    - "Erro ao carregar curso: {status_code} - {response_text}"
    - "Erro inesperado ao carregar curso: {error_message}"
    - "Erro ao adicionar disciplina: {status_code} - {response_text}"
    - "Erro inesperado ao adicionar disciplina: {error_message}"
    - "Todos os campos da disciplina são obrigatórios." se algum campo do formulário estiver vazio.
    - "Carga horária deve ser um número válido." se a carga horária não for um número.
    - "Nenhuma disciplina encontrada para este curso." se não houver disciplinas associadas ao curso.
    - "Disciplina adicionada com sucesso!" ao adicionar uma disciplina com sucesso.

    ### Parâmetros
    - pk (int): ID do curso a ser visualizado.
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        messages.error(
            request, "Você precisa estar logado para ver os detalhes do curso.")
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        request.session.flush()
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    try:
        with get_client(access) as api:
            curso_response = api.get(f'/cursos/{pk}/')  # Corrigido aqui
            curso_response.raise_for_status()
            curso = curso_response.json()

            # Lógica para adicionar disciplina
            if request.method == 'POST':
                nome = request.POST.get('nome')
                codigo = request.POST.get('codigo')
                carga_horaria = request.POST.get('carga_horaria')

                if not all([nome, codigo, carga_horaria]):
                    messages.error(
                        request, "Todos os campos da disciplina são obrigatórios.")
                    return redirect('curso_detail', pk=pk)

                try:
                    carga_horaria = int(carga_horaria)
                except ValueError:
                    messages.error(
                        request, "Carga horária deve ser um número válido.")
                    return redirect('curso_detail', pk=pk)

                data = {
                    'nome': nome,
                    'codigo': codigo,
                    'carga_horaria': carga_horaria,
                    'curso': pk,
                }
                try:
                    response = api.post(
                        # Ajustado aqui
                        f'{settings.INTERNAL_API_BASE_URL}/disciplinas/', json=data)
                    response.raise_for_status()
                    messages.success(
                        request, "Disciplina adicionada com sucesso!")
                    return redirect('curso_detail', pk=pk)
                except httpx.HTTPStatusError as e:
                    messages.error(
                        request, f"Erro ao adicionar disciplina: {e.response.status_code} - {e.response.text}")
                except Exception as e:
                    messages.error(
                        request, f"Erro inesperado ao adicionar disciplina: {e}")

            disciplinas = []
            try:
                disciplinas_url = f'/disciplinas/?curso={pk}'  # Corrigido aqui
                disciplinas_response = api.get(disciplinas_url)
                disciplinas_response.raise_for_status()
                disciplinas = disciplinas_response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    messages.info(
                        request, "Nenhuma disciplina encontrada para este curso.111111111")
                    disciplinas = []
                else:
                    raise

            total_disciplinas_ativas = 0
            soma_carga_horaria_disciplinas_ativas = 0
            if disciplinas.get('results'):
                total_disciplinas_ativas = len(disciplinas['results'])
                soma_carga_horaria_disciplinas_ativas = sum(
                    d.get('carga_horaria', 0) for d in disciplinas['results'])
            elif isinstance(disciplinas, list):
                total_disciplinas_ativas = len(disciplinas)
                soma_carga_horaria_disciplinas_ativas = sum(
                    d.get('carga_horaria', 0) for d in disciplinas)

            context = {
                'curso': curso,
                'disciplinas': disciplinas,
                'total_disciplinas_ativas': total_disciplinas_ativas,
                'soma_carga_horaria_disciplinas_ativas': soma_carga_horaria_disciplinas_ativas,
                'API_BASE_URL': settings.API_BASE_URL,
                'user_type': user_type,
            }
            return render(request, 'curso_detail.html', context)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            messages.error(
                request, "Você não tem permissão para acessar este curso.")
            request.session.flush()
            return redirect('login')
        elif e.response.status_code == 404:
            messages.error(request, "Curso não encontrado.")
            return redirect('index')
        else:
            messages.error(
                request, f"Erro ao carregar curso: {e.response.status_code} - {e.response.text}")
            return redirect('index')
    except Exception as e:
        messages.error(request, f"Erro inesperado ao carregar curso: {e}")
        return redirect('index')


@require_http_methods(["GET", "POST"])
def add_curso_view(request):
    """
    View para adicionar um novo curso.

    ### GET
    Renderiza a página de cursos.

    ### POST
    Processa o formulário para adicionar um novo curso.

    ### Mensagens de Erro
    - "Você não tem permissão para adicionar cursos." se o usuário não for do tipo 'Gerente'.
    - "Todos os campos são obrigatórios." se algum campo obrigatório estiver vazio.
    - "Carga horária deve ser um número válido." se a carga horária não for um número.
    - "Erro ao adicionar curso: {status_code} - {response_text}"
    - "Erro inesperado ao adicionar curso: {error_message}"
    - "Curso adicionado com sucesso!" ao adicionar com sucesso.
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    if user_type != 'Gerente':
        messages.error(
            request, "Você não tem permissão para adicionar cursos.")
        return redirect('cursos_list')

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        carga_horaria_total = request.POST.get('carga_horaria_total')

        if not all([codigo, nome, carga_horaria_total]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('cursos_list')

        try:
            carga_horaria_total = int(carga_horaria_total)
        except ValueError:
            messages.error(request, "Carga horária deve ser um número válido.")
            return redirect('cursos_list')

        data = {
            'codigo': codigo,
            'nome': nome,
            'descricao': descricao,
            'carga_horaria_total': carga_horaria_total,
            'ativo': True
        }

        try:
            with get_client(access) as api:
                response = api.post(
                    f'{settings.INTERNAL_API_BASE_URL}/cursos/', json=data)
                response.raise_for_status()
                messages.success(request, "Curso adicionado com sucesso!")
                return redirect('cursos_list')
        except httpx.HTTPStatusError as e:
            messages.error(
                request, f"Erro ao adicionar curso: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            messages.error(request, f"Erro inesperado ao adicionar curso: {e}")

    return redirect('cursos_list')


@require_http_methods(["GET", "POST"])
def edit_curso_view(request, pk):
    """
    View para editar um curso existente.

    ### GET
    Renderiza a página de cursos.

    ### POST
    Processa o formulário para editar um curso.

    ### Mensagens de Erro
    - "Você não tem permissão para editar cursos." se o usuário não for do tipo 'Gerente'.
    - "Todos os campos são obrigatórios." se algum campo obrigatório estiver vazio.
    - "Carga horária deve ser um número válido." se a carga horária não for um número.
    - "Erro ao atualizar curso: {status_code} - {response_text}"
    - "Erro inesperado ao atualizar curso: {error_message}"
    - "Curso atualizado com sucesso!" ao atualizar com sucesso.

    ### Parâmetros
    - pk (int): ID do curso a ser editado.
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    if user_type != 'Gerente':
        messages.error(request, "Você não tem permissão para editar cursos.")
        return redirect('cursos_list')

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        carga_horaria_total = request.POST.get('carga_horaria_total')
        ativo = request.POST.get('ativo') == 'on'

        if not all([codigo, nome, carga_horaria_total]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('cursos_list')

        try:
            carga_horaria_total = int(carga_horaria_total)
        except ValueError:
            messages.error(request, "Carga horária deve ser um número válido.")
            return redirect('cursos_list')

        data = {
            'codigo': codigo,
            'nome': nome,
            'descricao': descricao,
            'carga_horaria_total': carga_horaria_total,
            'ativo': ativo
        }

        try:
            with get_client(access) as api:
                response = api.put(
                    f'{settings.INTERNAL_API_BASE_URL}/cursos/{pk}/', json=data)
                response.raise_for_status()
                messages.success(request, "Curso atualizado com sucesso!")
                return redirect('cursos_list')
        except httpx.HTTPStatusError as e:
            messages.error(
                request, f"Erro ao atualizar curso: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            messages.error(request, f"Erro inesperado ao atualizar curso: {e}")

    return redirect('cursos_list')


@require_http_methods(["GET", "POST"])
def add_perfil_view(request):
    """
    View para adicionar um novo perfil.

    ### GET
    Renderiza a página de perfis.

    ### POST
    Processa o formulário para adicionar um novo perfil.

    ### Mensagens de Erro
    - "Você não tem permissão para adicionar perfis." se o usuário não for do tipo 'Gerente'.
    - "Todos os campos são obrigatórios." se algum campo obrigatório estiver vazio.
    - "Email deve ser um endereço válido." se o email não for válido.
    - "Erro ao adicionar perfil: {status_code} - {response_text}"
    - "Erro inesperado ao adicionar perfil: {error_message}"
    - "Perfil adicionado com sucesso!" ao adicionar com sucesso.
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    if user_type != 'Gerente':
        messages.error(
            request, "Você não tem permissão para adicionar perfis.")
        return redirect('perfis_list')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo = request.POST.get('tipo')

        if not all([nome, email, password, tipo]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('perfis_list')

        data = {
            'nome': nome,
            'email': email,
            'password': password,
            'tipo': tipo,
            'ativo': True
        }

        try:
            with get_client(access) as api:
                response = api.post(
                    f'{settings.INTERNAL_API_BASE_URL}/perfis/', json=data)
                response.raise_for_status()
                messages.success(request, "Perfil adicionado com sucesso!")
                return redirect('perfis_list')
        except httpx.HTTPStatusError as e:
            messages.error(
                request, f"Erro ao adicionar perfil: {e.response.status_code} - {e.response.text}")
            return redirect('perfis_list')
        except Exception as e:
            messages.error(
                request, f"Erro inesperado ao adicionar perfil: {e}")
            return redirect('perfis_list')

    return redirect('perfis_list')


@require_http_methods(["GET", "POST"])
def edit_perfil_view(request, pk):
    """
    View para editar um perfil existente.

    ### GET
    Renderiza a página de perfis.

    ### POST
    Processa o formulário para editar um perfil.

    ### Mensagens de Erro
    - "Você não tem permissão para editar perfis." se o usuário não for do tipo 'Gerente'.
    - "Todos os campos são obrigatórios." se algum campo obrigatório estiver vazio.
    - "Email deve ser um endereço válido." se o email não for válido.
    - "Erro ao atualizar perfil: {status_code} - {response_text}"
    - "Erro inesperado ao atualizar perfil: {error_message}"
    - "Perfil atualizado com sucesso!" ao atualizar com sucesso.

    ### Parâmetros
    - pk (int): ID do perfil a ser editado.
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    if user_type != 'Gerente':
        messages.error(request, "Você não tem permissão para editar perfis.")
        return redirect('perfis_list')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        tipo = request.POST.get('tipo')
        ativo = request.POST.get('ativo') == 'on'

        if not all([nome, email, tipo]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('perfis_list')

        data = {
            'nome': nome,
            'email': email,
            'tipo': tipo,
            'ativo': ativo
        }

        try:
            with get_client(access) as api:
                response = api.put(
                    f'{settings.INTERNAL_API_BASE_URL}/perfis/{pk}/', json=data)
                response.raise_for_status()
                messages.success(request, "Perfil atualizado com sucesso!")
                return redirect('perfis_list')
        except httpx.HTTPStatusError as e:
            messages.error(
                request, f"Erro ao atualizar perfil: {e.response.status_code} - {e.response.text}")
            return redirect('perfis_list')
        except Exception as e:
            messages.error(
                request, f"Erro inesperado ao atualizar perfil: {e}")
            return redirect('perfis_list')

    return redirect('perfis_list')


@require_http_methods(["POST"])
def toggle_perfil_ativo_view(request, pk):
    """
    View para ativar/inativar um perfil.

    ### POST
    Processa a ativação/inativação de um perfil.

    ### Mensagens de Erro
    - "Você não tem permissão para alterar status de perfis." se o usuário não for do tipo 'Gerente'.
    - "Erro ao alterar status do perfil: {status_code} - {response_text}"
    - "Erro inesperado ao alterar status do perfil: {error_message}"
    - "Perfil ativado com sucesso!" ou "Perfil inativado com sucesso!" ao alterar com sucesso.

    ### Parâmetros
    - pk (int): ID do perfil a ser alterado.
    """
    access, refresh = _get_tokens(request.session)
    if not access:
        return redirect('login')

    user_type = None
    try:
        user_profile = get_user_profile(access)
        user_type = user_profile.get('tipo')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
        return redirect('login')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao obter perfil do usuário: {e}")
        request.session.flush()
        return redirect('login')

    if user_type != 'Gerente':
        messages.error(
            request, "Você não tem permissão para alterar status de perfis.")
        return redirect('perfis_list')

    ativo = request.POST.get('ativo') == 'true'
    action = 'ativar' if ativo else 'inativar'

    try:
        with get_client(access) as api:
            response = api.patch(
                f'{settings.INTERNAL_API_BASE_URL}/perfis/{pk}/{action}/', json={'ativo': ativo})
            response.raise_for_status()
            messages.success(request, f"Perfil {action}do com sucesso!")
            return redirect('perfis_list')
    except httpx.HTTPStatusError as e:
        messages.error(
            request, f"Erro ao alterar status do perfil: {e.response.status_code} - {e.response.text}")
        return redirect('perfis_list')
    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao alterar status do perfil: {e}")
        return redirect('perfis_list')
