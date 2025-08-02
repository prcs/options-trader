# analyzer_risco_retorno.py

def avaliar_risco_retorno(premio_recebido: float, risco_maximo: float) -> dict:
    """
    Avalia a atratividade da relação risco/retorno da estratégia.
    """
    if risco_maximo == 0:
        return {"score": 0, "comentario": "Risco máximo é zero (inválido)."}

    relacao = premio_recebido / risco_maximo

    if relacao >= 0.5:
        score = 1.0
        comentario = "Excelente relação risco/retorno."
    elif relacao >= 0.35:
        score = 0.7
        comentario = "Boa relação risco/retorno."
    elif relacao >= 0.25:
        score = 0.5
        comentario = "Relação razoável, mas atenção ao risco."
    else:
        score = 0.2
        comentario = "Relação risco/retorno desfavorável."

    return {
        "score": score,
        "comentario": comentario,
        "relacao": round(relacao, 2)
    }
