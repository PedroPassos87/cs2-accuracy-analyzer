import pandas as pd
from awpy import Demo
from awpy.stats import adr

def demo(caminho_demo: str) -> dict | None:
    """
    Carrega e faz o parse de um arquivo de demo do CS, 
    retornando os dados em um dicionário de DataFrames.
    Lida com a ausência de certos eventos em demos de CS2.
    """
    print(f"Iniciando o parse da demo: {caminho_demo}...")
    try:
        dem = Demo(path=caminho_demo, verbose=True)
        dem.parse()
        print("\nParse principal concluído. Coletando e retornando dados...")
        print(f"ADR: {adr(dem)}")
        dados_processados = {}
        atributos = [
            "header", "rounds", "kills", "damages", "shots",
            "bomb", "smokes", "infernos", "grenades", "footsteps", "ticks"
        ]

        for attr in atributos:
            try:
                dados_processados[attr] = getattr(dem, attr)
            except Exception:
                # Se falhar, simplesmente não adiciona a chave ao dicionário.
                pass
        
        return dados_processados

    except Exception as e:
        print(f"Ocorreu um erro CRÍTICO durante o parse da demo: {e}")
        return None

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    
    caminho_do_meu_arquivo = "D:/analisedados/cs2-accuracy-analyzer/cs2_heatmap/demos/mirage_inatel_suns.dem"
    
    # 1. Executa a função robusta que retorna um dicionário
    dados_da_demo = demo(caminho_demo=caminho_do_meu_arquivo)

    # 2. Verifica se o dicionário não está vazio e começa a exibir os dados
    if dados_da_demo:
        print("\n------------------ EXIBINDO DADOS (n=7) ------------------")
        
        # Para cada chave no dicionário, tentamos imprimir os dados.
        # Isso garante que só vamos imprimir o que foi coletado com sucesso.
        
        # Usamos ['chave'] para acessar dados de um dicionário.
        
        if "header" in dados_da_demo:
            print(f"\nHeader: \n{dados_da_demo['header']}")

        if "rounds" in dados_da_demo:
            print(f"\nRounds: \n{dados_da_demo['rounds'].head(n=7)}")
            
        if "kills" in dados_da_demo:
            print(f"\nKills: \n{dados_da_demo['kills'].head(n=7)}")

        if "damages" in dados_da_demo:
            print(f"\nDamages: \n{dados_da_demo['damages'].head(n=7)}")

        if "shots" in dados_da_demo:
            # Renomeado para 'shots' para corresponder à chave do dicionário
            print(f"\nWeapon Fires: \n{dados_da_demo['shots'].head(n=7)}")

        if "bomb" in dados_da_demo:
            print(f"\nBomb: \n{dados_da_demo['bomb'].head(n=7)}")
            
        if "smokes" in dados_da_demo:
            print(f"\nSmokes: \n{dados_da_demo['smokes'].head(n=7)}")

        if "infernos" in dados_da_demo:
            print(f"\nInfernos: \n{dados_da_demo['infernos'].head(n=7)}")

        if "grenades" in dados_da_demo:
            print(f"\nGrenades: \n{dados_da_demo['grenades'].head(n=7)}")
            
        if "footsteps" in dados_da_demo:
            print(f"\nFootsteps: \n{dados_da_demo['footsteps'].head(n=7)}")
        else:
            # Se 'footsteps' não existir no dicionário, apenas informa o usuário.
            print("\nFootsteps: \n[!] Dados de passos não encontrados ou não puderam ser processados.")

        if "ticks" in dados_da_demo:
            print(f"\nTicks: \n{dados_da_demo['ticks'].head(n=7)}")


    else:
        print("\nA função não retornou dados devido a um erro crítico.")