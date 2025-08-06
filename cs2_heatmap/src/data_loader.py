import pandas as pd
from awpy import Demo

def parse_demo(caminho_demo: str) -> dict:
    """
    Carrega e faz o parse de um arquivo de demo do CS, retornando os dados em um dicionário.
    """
    print(f"Iniciando o parse da demo: {caminho_demo}...")
    try:
        # Usamos o parse_rate=128 para uma boa granularidade de posições
        dem = Demo(demofile=caminho_demo,verbose=False)
        data = dem.parse()
        print("Parse da demo concluído com sucesso!")
        return data
    except Exception as e:
        print(f"Ocorreu um erro ao fazer o parse da demo: {e}")
        return None