from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from .services import get_client, obtain_token, refresh_token, get_user_profile
import httpx


def _get_tokens(session):
    return session.get('access'), session.get('refresh')


def _save_tokens(session, access: str, refresh: str | None = None):
    session['access'] = access
    if refresh:
        session['refresh'] = refresh


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            tokens = obtain_token(email, password)
            _save_tokens(request.session, tokens['access'], tokens['refresh'])
            return redirect('index')
        except httpx.HTTPStatusError as e:
            messages.error(
                request, f"Login falhou: {e.response.status_code} - {e.response.text}")
        except Exception as e:  # Captura exceções gerais
            print(f"[DEBUG - Frontend - Login] Erro inesperado: {e}")  # DEBUG
            messages.error(request, f"Erro inesperado ao tentar logar: {e}")
    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def home_view(request):
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
        messages.error(
            request, f"Erro ao obter perfil do usuário: {e.response.status_code} - {e.response.text}")
        request.session.flush()
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
                        f'{settings.API_BASE_URL}/disciplinas/', json=data)
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
                        request, "Nenhuma disciplina encontrada para este curso.")
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
