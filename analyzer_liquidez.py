# analyzer_liquidez.py

def avaliar_liquidez(volume_total: int, spread_medio: float) -> dict:
    """
    Avalia a liquidez da estrutura com base no volume e no spread médio.
    """
    if volume_total == 0:
        return {"score": 0, "comentario": "Sem liquidez"}

    if spread_medio < 0.05:
        score = 1.0
        comentario = "Alta liquidez e spread baixo"
    elif spread_medio < 0.15:
        score = 0.7
        comentario = "Liquidez aceitável"
    elif spread_medio < 0.30:
        score = 0.4
        comentario = "Liquidez baixa"
    else:
        score = 0.1
        comentario = "Liquidez muito ruim"

    return {
        "score": score,
        "comentario": comentario,
        "spread": spread_medio,
        "volume_total": volume_total
    }
