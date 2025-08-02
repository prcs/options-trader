# auth.py

import requests

BASE_URL = "https://api.oplab.com.br/v3"
LOGIN_ENDPOINT = "/domain/users/authenticate?for=default"

def autenticar(email: str, senha: str) -> str:
    """
    Retorna o access-token válido para uso nas demais requisições da API da Oplab.
    """
    payload = {"email": email, "password": senha}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(BASE_URL + LOGIN_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()["access-token"]
