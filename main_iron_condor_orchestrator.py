# main_iron_condor_orchestrator.py

from typing import Optional, List
# Import corrigido para utilizar o coletor de opções disponível no projeto
from fetch_options import obter_opcoes_ativo
from iv_rank_analyzer import calcular_iv_rank_percentil, gerar_simulacao_iv_historico
from iron_condor_selector import avaliar_combinacoes_iron_condor


def orquestrar_iron_condor(
    ativo: str,
    access_token: str,
    vencimento: Optional[str] = None,
    iv_atual: float = 35.0,
    usar_simulacao_iv: bool = True
) -> List[dict]:
    """
    Orquestrador geral da estratégia Iron Condor para um determinado ativo.

    Parâmetros:
    - ativo: Ticker da ação (ex: 'PETR4')
    - access_token: Token de acesso à API da Oplab
    - vencimento: Data de vencimento desejada (ex: '2025-08-16') ou None para todos
    - iv_atual: IV atual do ativo (opcional, será usado para cálculo de IV Rank)
    - usar_simulacao_iv: Se True, gera histórico simulado. Futuramente trocar por dados reais.

    Retorno:
    Lista de estruturas Iron Condor avaliadas.
    """

    print(f"Buscando opções para o ativo {ativo}...")
    opcoes = obter_opcoes_ativo(ativo, access_token)

    if vencimento:
        opcoes = [o for o in opcoes if o["vencimento"] == vencimento]

    if usar_simulacao_iv:
        historico_iv = gerar_simulacao_iv_historico(iv_atual)
    else:
        raise NotImplementedError("Histórico real de IV ainda não implementado.")

    iv_rank, iv_percentil = calcular_iv_rank_percentil(historico_iv, iv_atual)

    print(f"IV Rank: {iv_rank}, IV Percentil: {iv_percentil}")
    print("Gerando e avaliando combinações de Iron Condor...")

    melhores_estrategias = avaliar_combinacoes_iron_condor(opcoes, iv_rank, iv_percentil)

    return melhores_estrategias
