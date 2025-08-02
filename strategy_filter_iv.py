# strategy_filter_iv.py

def avaliar_iv_para_iron_condor(iv_rank: float, iv_percentil: float) -> dict:
    """
    Avalia se o nível de IV atual justifica montar um Iron Condor.
    IVs muito baixos indicam má remuneração pelo risco.
    """
    score_iv = round((iv_rank + iv_percentil) / 2, 2)

    comentario = "IV alto, bom para venda de volatilidade" if score_iv > 0.6 else (
        "IV moderado, risco controlado" if score_iv > 0.4 else "IV baixo, estratégia arriscada"
    )

    return {"score": score_iv, "comentario": comentario}
