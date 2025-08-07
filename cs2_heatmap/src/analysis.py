# src/analysis.py
import polars as pl
import pandas as pd
from awpy.demo import Demo

def extrair_posicoes_jogador(demo_obj: Demo, nomes_jogadores: list, lado: str) -> pd.DataFrame:
    """
    Extrai as posições (x, y) de um jogador usando a filtragem de DataFrame do Polars.
    """
    print(f"Extraindo posições para '{', '.join(nomes_jogadores)}' no lado '{lado}'...")

    # MUDANÇA FUNDAMENTAL: Usamos Polars para filtrar o DataFrame de ticks
    # Esta é a maneira correta e muito mais rápida
    if not hasattr(demo_obj, 'ticks') or demo_obj.ticks is None:
        print("DataFrame de ticks não encontrado na demo.")
        return pd.DataFrame()

    try:
        # Filtra o DataFrame de ticks para as condições desejadas:
        # 1. O nome do jogador está na nossa lista
        # 2. O lado (CT/T) corresponde ao que queremos
        posicoes_pl = demo_obj.ticks.filter(
            (pl.col("name").is_in(nomes_jogadores)) &
            (pl.col("side") == lado.lower())
        ).select(["x", "y", "z"]) # Seleciona apenas as colunas de posição

        if posicoes_pl.is_empty():
            print(f"Nenhuma posição encontrada para '{', '.join(nomes_jogadores)}' no lado '{lado}'.")
            return pd.DataFrame()

        print(f"{len(posicoes_pl)} posições encontradas.")
        
        # O visualizador espera um DataFrame do Pandas, então convertemos no final
        return posicoes_pl.to_pandas()

    except Exception as e:
        print(f"Ocorreu um erro ao filtrar o DataFrame de ticks: {e}")
        return pd.DataFrame()