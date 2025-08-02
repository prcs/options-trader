# fetch_stock.py

import requests

BASE_URL = "https://api.oplab.com.br/v3"

def obter_dados_acao(ticker_base: str, access_token: str) -> dict:
    """
    Retorna as informações da ação base, como preço atual (spot), nome, código, etc.
    """
    url = f"{BASE_URL}/market/stocks/{ticker_base}"
    headers = {"accept": "application/json", "Access-Token": access_token}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()
