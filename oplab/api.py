import requests
import pandas as pd

def autenticar_oplab(email: str, senha: str) -> dict:
    url = "https://api.oplab.com.br/v3/domain/users/authenticate?for=default"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "password": senha
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    dados = response.json()

    # Coletar dados principais
    access_token = dados.get("access-token")
    juros = dados.get("preferences", {}).get("interest_rate_value")
    tipo_juros = dados.get("preferences", {}).get("interest_rate_type")

    return {
        "access_token": access_token,
        "juros": juros,
        "tipo_juros": tipo_juros,
        "nome": dados.get("name"),
        "usuario_id": dados.get("id"),
        "raw": dados
    }

# Exemplo de uso:
login = autenticar_oplab("peterson_@live.com", "Ps$120454")
print(f"Access Token: {login['access_token']}")
print(f"Taxa de Juros: {login['juros']} ({login['tipo_juros']})")


ACCESS_TOKEN = login['access_token']
HEADERS = {
    "accept": "application/json",
    "Access-Token": ACCESS_TOKEN
}

def get_options(symbol: str) -> pd.DataFrame:
    url = f"https://api.oplab.com.br/v3/market/options/{symbol}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # lança erro caso status != 200
    data = response.json()
    return pd.DataFrame(data)

# Exemplo de uso
df_opcoes = get_options("PETR4")

# Visualizar primeiras linhas
print(df_opcoes[["symbol", "strike", "type", "due_date", "bid", "ask", "close", "spot_price"]].head())


def arredondar_meio(valor):
    return round(valor * 2) / 2

def calcular_black_scholes(symbol, irate, spotprice=0, strike=0, premium=0, dtm=0, vol=0, amount=0):
    url = "https://api.oplab.com.br/v3/market/options/bs"
    params = {
        "symbol": symbol,
        "irate": irate,          # taxa livre de risco anualizada (ex: 0.13)
        "spotprice": spotprice,  # preço do ativo-objeto
        "strike": strike,        # strike da opção
        "premium": premium,      # prêmio da opção (preço de mercado)
        "dtm": dtm,              # dias úteis até o vencimento
        "vol": vol,              # volatilidade implícita anualizada (ex: 0.34)
        "amount": amount         # tamanho do contrato (100 normalmente)
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

# Exemplo de chamada:
resultado = calcular_black_scholes(
    symbol="PETRH340",
    irate=arredondar_meio(login['juros'])/100,
)

print(resultado)
