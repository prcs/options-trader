# main.py

from iv_rank_analyzer import calcular_iv_rank_percentil, gerar_simulacao_iv_historico, contexto_favoravel_iron_condor
from analyzer_risco_retorno import avaliar_risco_retorno
from analyzer_liquidez import avaliar_liquidez
from strategy_filter_iv import avaliar_iv_para_iron_condor

# Exemplo de dados simulados
iv_atual = 32.5
historico_iv = gerar_simulacao_iv_historico(iv_atual)
premio_recebido = 1.2
risco_maximo = 3.8
volume_total = 50000
spread_medio = 0.05

# Passo 1: Cálculo do IV Rank e IV Percentil
iv_rank, iv_percentil = calcular_iv_rank_percentil(historico_iv, iv_atual)
print("IV Rank:", iv_rank, "IV Percentil:", iv_percentil)

# Passo 2: Avaliação da atratividade com base no IV
resultado_iv = avaliar_iv_para_iron_condor(iv_rank, iv_percentil)
print("Análise de IV:", resultado_iv)

# Passo 3: Avaliação risco/retorno
resultado_risco = avaliar_risco_retorno(premio_recebido, risco_maximo)
print("Análise Risco/Retorno:", resultado_risco)

# Passo 4: Avaliação de liquidez
resultado_liquidez = avaliar_liquidez(volume_total, spread_medio)
print("Análise de Liquidez:", resultado_liquidez)

# Passo 5: Contexto favorável de tendência (simulação com ativo PETR4)
import yfinance as yf
import pandas_ta as ta

df = yf.download("PETR4.SA", period="60d", interval="1d")
contexto_ok = contexto_favoravel_iron_condor(df)
print("Contexto de lateralização:", "Sim" if contexto_ok else "Não")

# Score final (peso exemplo)
pesos = {"iv": 0.4, "risco_retorno": 0.4, "liquidez": 0.2}
score_total = (
    pesos["iv"] * resultado_iv["score"] +
    pesos["risco_retorno"] * resultado_risco["score"] +
    pesos["liquidez"] * resultado_liquidez["score"]
)

print("Score Final:", round(score_total, 2))
print("Recomendação:", "Montar" if score_total >= 0.6 and contexto_ok else "Evitar")
