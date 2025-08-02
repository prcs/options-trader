# iron_condor_builder.py

from typing import List, Dict, Optional
from datetime import datetime
from itertools import product
from analyzer_iron_condor import avaliar_estrategia_iron_condor

def filtrar_opcoes_por_tipo_e_vencimento(lista: List[dict], tipo: str, vencimento: str) -> List[dict]:
    """
    Retorna uma lista de opções filtradas por tipo (CALL ou PUT) e vencimento.
    """
    return [
        op for op in lista
        if op["type"] == tipo and op["due_date"] == vencimento
    ]

def montar_combinacoes_iron_condor(lista_opcoes: List[dict], multiplicador: float = 1.0) -> List[Dict]:
    """
    Monta todas as combinações possíveis de Iron Condor para um mesmo vencimento.
    """
    resultados = []

    # Identifica vencimentos únicos disponíveis
    vencimentos = sorted({op["due_date"] for op in lista_opcoes})

    for vencimento in vencimentos:
        calls = sorted(filtrar_opcoes_por_tipo_e_vencimento(lista_opcoes, "CALL", vencimento), key=lambda x: x["strike"])
        puts  = sorted(filtrar_opcoes_por_tipo_e_vencimento(lista_opcoes, "PUT", vencimento), key=lambda x: x["strike"], reverse=True)

        for call_vendida, call_comprada in product(calls, calls):
            if call_comprada["strike"] <= call_vendida["strike"]:
                continue

            for put_vendida, put_comprada in product(puts, puts):
                if put_comprada["strike"] >= put_vendida["strike"]:
                    continue

                strike_range = call_comprada["strike"] - call_vendida["strike"]
                if strike_range != (put_vendida["strike"] - put_comprada["strike"]):
                    continue  # Mantém simetria

                # Cálculo de prêmio recebido (credit spread)
                premio = (
                    call_vendida["bid"] - call_comprada["ask"] +
                    put_vendida["bid"] - put_comprada["ask"]
                ) * multiplicador

                if premio <= 0:
                    continue  # Não vale a pena

                risco = strike_range * 1.0 * multiplicador - premio

                volume_total = sum([
                    call_vendida["volume"],
                    call_comprada["volume"],
                    put_vendida["volume"],
                    put_comprada["volume"]
                ])

                spread_medio = (
                    (call_vendida["ask"] - call_vendida["bid"]) +
                    (call_comprada["ask"] - call_comprada["bid"]) +
                    (put_vendida["ask"] - put_vendida["bid"]) +
                    (put_comprada["ask"] - put_comprada["bid"])
                ) / 4

                iv_rank = call_vendida.get("iv_rank", 0.5)  # Placeholder, sobrescreva com valor real
                iv_percentil = call_vendida.get("iv_percentil", 0.5)

                resultado = avaliar_estrategia_iron_condor(
                    iv_rank=iv_rank,
                    iv_percentil=iv_percentil,
                    premio_recebido=premio,
                    risco_maximo=risco,
                    volume_total=volume_total,
                    spread_medio=spread_medio
                )

                resultados.append({
                    "ticker_call_vendida": call_vendida["symbol"],
                    "ticker_call_comprada": call_comprada["symbol"],
                    "ticker_put_vendida": put_vendida["symbol"],
                    "ticker_put_comprada": put_comprada["symbol"],
                    "vencimento": vencimento,
                    "premio_recebido": round(premio, 2),
                    "risco_maximo": round(risco, 2),
                    "score_final": resultado["score_total"],
                    "iv_rank": iv_rank,
                    "liquidez_aprovada": resultado["analises"]["liquidez"]["aprovado"],
                    "recomendacao": resultado["recomendacao"],
                    "comentarios": resultado["analises"]["iv"]["comentarios"]
                })

    return sorted(resultados, key=lambda x: x["score_final"], reverse=True)
