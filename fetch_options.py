# fetch_options.py

import requests

BASE_URL = "https://api.oplab.com.br/v3"

def obter_opcoes_ativo(ticker_base: str, access_token: str) -> list:
    """
    Retorna todas as opções (calls e puts) de um ativo base (ex: PETR4).
    """
    url = f"{BASE_URL}/market/options/{ticker_base}"
    headers = {"accept": "application/json", "Access-Token": access_token}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()
