# iv_rank_analyzer.py

import pandas as pd
import numpy as np
from typing import Tuple
import pandas_ta as ta

def calcular_iv_rank_percentil(series_iv: pd.Series, iv_atual: float) -> Tuple[float, float]:
    """
    Calcula o IV Rank e o IV Percentil com base em uma série histórica de IVs e o IV atual.

    IV Rank: (IV atual - IV mínimo) / (IV máximo - IV mínimo)
    IV Percentil: Percentual de valores na série que estão abaixo do IV atual
    """
    if len(series_iv) < 10:
        raise ValueError("Histórico de IV insuficiente para análise.")

    iv_min = series_iv.min()
    iv_max = series_iv.max()
    iv_rank = round((iv_atual - iv_min) / (iv_max - iv_min + 1e-8), 2)

    iv_percentil = round((series_iv < iv_atual).sum() / len(series_iv), 2)

    return iv_rank, iv_percentil

def gerar_simulacao_iv_historico(iv_atual: float, dias: int = 100) -> pd.Series:
    """
    (Simulação temporária) Gera série fictícia de IV para testes com ruído em torno do IV atual.
    Substituir futuramente por dados reais.
    """
    np.random.seed(42)
    historico = np.random.normal(loc=iv_atual, scale=5, size=dias)
    historico = np.clip(historico, 5, 90)
    return pd.Series(historico)

def contexto_favoravel_iron_condor(df_precos: pd.DataFrame) -> bool:
    """
    Verifica se o ativo está em contexto lateralizado favorável ao Iron Condor:
    - RSI entre 45 e 55
    - Preço dentro das bandas de Bollinger
    - Baixa volatilidade (Bollinger Bandwidth abaixo de 10%)

    Requer um DataFrame com colunas ['close'] e index temporal.
    """
    if df_precos.shape[0] < 20:
        return False

    df = df_precos.copy()
    df['rsi'] = ta.rsi(df['close'], length=14)
    bb = ta.bbands(df['close'], length=20, std=2)
    df['bb_upper'] = bb['BBU_20_2.0']
    df['bb_lower'] = bb['BBL_20_2.0']
    df['bb_bandwidth'] = (df['bb_upper'] - df['bb_lower']) / df['close'] * 100

    rsi_final = df['rsi'].iloc[-1]
    close = df['close'].iloc[-1]
    upper = df['bb_upper'].iloc[-1]
    lower = df['bb_lower'].iloc[-1]
    bandwidth = df['bb_bandwidth'].iloc[-1]

    lateralizado = (45 <= rsi_final <= 55)
    dentro_band = (lower <= close <= upper)
    vol_baixa = (bandwidth < 10)

    return lateralizado and dentro_band and vol_baixa
