# iron_condor_analyzer.py

from strategy_filter_iv import avaliar_iv_para_iron_condor
from analyzer_risco_retorno import avaliar_risco_retorno
from analyzer_liquidez import avaliar_liquidez

def avaliar_estrategia_iron_condor(
    iv_rank: float,
    iv_percentil: float,
    premio_recebido: float,
    risco_maximo: float,
    volume_total: int,
    spread_medio: float,
    pesos: dict = None
) -> dict:
    """
    Avaliação composta da estratégia Iron Condor com base em IV, risco/retorno e liquidez.
    """

    if pesos is None:
        pesos = {
            "iv": 0.4,
            "risco_retorno": 0.4,
            "liquidez": 0.2
        }

    resultado_iv = avaliar_iv_para_iron_condor(iv_rank, iv_percentil)
    resultado_risco = avaliar_risco_retorno(premio_recebido, risco_maximo)
    resultado_liquidez = avaliar_liquidez(volume_total, spread_medio)

    score_total = (
        pesos["iv"] * resultado_iv["score"] +
        pesos["risco_retorno"] * resultado_risco["score"] +
        pesos["liquidez"] * resultado_liquidez["score"]
    )

    if score_total >= 0.75:
        recomendacao = "Montar"
    elif score_total >= 0.6:
        recomendacao = "Montar com cautela"
    else:
        recomendacao = "Evitar"

    return {
        "score_total": round(score_total, 2),
        "analises": {
            "iv": resultado_iv,
            "risco_retorno": resultado_risco,
            "liquidez": resultado_liquidez
        },
        "recomendacao": recomendacao,
        "comentarios": f"{resultado_iv['comentario']}, {resultado_risco['comentario']}, {resultado_liquidez['comentario']}"
    }
