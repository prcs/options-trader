# iron_condor_selector.py

from itertools import combinations
from typing import List, Dict
from iron_condor_analyzer import avaliar_estrategia_iron_condor

def montar_combinacoes_validas(opcoes: List[Dict]) -> List[Dict]:
    """
    Gera combinações válidas de Iron Condor: venda/compra de CALLs e venda/compra de PUTs com strikes diferentes.
    """
    calls = [o for o in opcoes if o["tipo"] == "CALL"]
    puts = [o for o in opcoes if o["tipo"] == "PUT"]

    combinacoes = []

    for call_venda, call_compra in combinations(calls, 2):
        if call_venda["strike"] >= call_compra["strike"]:
            continue

        for put_venda, put_compra in combinations(puts, 2):
            if put_venda["strike"] <= put_compra["strike"]:
                continue

            if call_venda["vencimento"] != call_compra["vencimento"] or \
               put_venda["vencimento"] != put_compra["vencimento"] or \
               call_venda["vencimento"] != put_venda["vencimento"]:
                continue

            combinacoes.append({
                "call_vendida": call_venda,
                "call_comprada": call_compra,
                "put_vendida": put_venda,
                "put_comprada": put_compra,
                "vencimento": call_venda["vencimento"]
            })

    return combinacoes


def avaliar_combinacoes_iron_condor(opcoes: List[Dict], iv_rank: float, iv_percentil: float) -> List[Dict]:
    """
    Avalia todas as combinações possíveis de Iron Condor para um conjunto de opções.
    Retorna uma lista de estratégias com score final e recomendação.
    """

    combinacoes = montar_combinacoes_validas(opcoes)
    resultados = []

    for c in combinacoes:
        # Premissas: prêmio total recebido (soma dos prêmios vendidos - comprados)
        premio = (
            c["call_vendida"]["preco"] - c["call_comprada"]["preco"] +
            c["put_vendida"]["preco"] - c["put_comprada"]["preco"]
        )

        risco = max(
            c["call_comprada"]["strike"] - c["call_vendida"]["strike"],
            c["put_vendida"]["strike"] - c["put_comprada"]["strike"]
        ) - premio

        volume_total = sum([
            c["call_vendida"]["volume"],
            c["call_comprada"]["volume"],
            c["put_vendida"]["volume"],
            c["put_comprada"]["volume"]
        ])

        spread_medio = sum([
            abs(c["call_vendida"]["ask"] - c["call_vendida"]["bid"]),
            abs(c["call_comprada"]["ask"] - c["call_comprada"]["bid"]),
            abs(c["put_vendida"]["ask"] - c["put_vendida"]["bid"]),
            abs(c["put_comprada"]["ask"] - c["put_comprada"]["bid"]),
        ]) / 4

        analise = avaliar_estrategia_iron_condor(
            iv_rank=iv_rank,
            iv_percentil=iv_percentil,
            premio_recebido=round(premio, 2),
            risco_maximo=round(risco, 2),
            volume_total=volume_total,
            spread_medio=spread_medio
        )

        resultados.append({
            "ticker_call_vendida": c["call_vendida"]["ticker"],
            "ticker_call_comprada": c["call_comprada"]["ticker"],
            "ticker_put_vendida": c["put_vendida"]["ticker"],
            "ticker_put_comprada": c["put_comprada"]["ticker"],
            "vencimento": c["vencimento"],
            "premio_recebido": round(premio, 2),
            "risco_maximo": round(risco, 2),
            "score_final": analise["score_total"],
            "iv_rank": iv_rank,
            "liquidez_aprovada": analise["analises"]["liquidez"]["aprovado"],
            "recomendacao": analise["recomendacao"],
            "comentarios": analise["comentarios"]
        })

    # Ordenar do melhor para o pior
    resultados = sorted(resultados, key=lambda x: x["score_final"], reverse=True)

    return resultados
