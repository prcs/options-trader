# coletor_opcoes_oplab.py

import requests
from typing import List

OPLAB_API_URL = "https://api.oplab.com.br/v3"
TOKEN = "SEU_TOKEN_AQUI"  # Troque por seu token válido

def obter_opcoes_do_ativo(ticker: str) -> List[dict]:
    """
    Retorna todas as opções disponíveis para o ativo especificado via OpLab.

    :param ticker: Código do ativo (ex: PETR4)
    :return: Lista de dicionários com dados das opções
    """
    url = f"{OPLAB_API_URL}/market/options/{ticker.upper()}"
    headers = {
        "accept": "application/json",
        "Access-Token": TOKEN
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        opcoes = response.json()
        return opcoes
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar opções do ativo {ticker}: {e}")
        return []
