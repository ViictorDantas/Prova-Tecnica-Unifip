from typing import Optional
import httpx
from django.conf import settings

def get_client(access_token: str | None = None) -> httpx.Client:
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return httpx.Client(base_url=settings.INTERNAL_API_BASE_URL, headers=headers, timeout=10)

def obtain_token(email: str, password: str) -> dict:
    with httpx.Client(timeout=10) as c:
        r = c.post(settings.API_TOKEN_URL, json={"email": email, "password": password})
        r.raise_for_status()
        return r.json()

def refresh_token(refresh: str) -> dict:
    with httpx.Client(timeout=10) as c:
        r = c.post(settings.API_REFRESH_URL, json={'refresh': refresh})
        r.raise_for_status()
        return r.json()

def get_user_profile(access_token: str) -> dict:
    with get_client(access_token) as api:
        r = api.get('/perfis/me/')
        r.raise_for_status()
        return r.json()