# src/main.py

import json
import os
from data_loader import parse_demo
from analysis import extrair_posicoes_jogador
from visualizer import criar_heatmap_posicionamento

def selecionar_jogador(demo_obj) -> str:
    """
    Lista os jogadores da partida e pede para o usuário selecionar um.
    """
    # MUDANÇA DEFINITIVA: A lista de jogadores é extraída do DataFrame 'ticks', que contém
    # todas as informações de todos os jogadores em todos os momentos do jogo.
    if not hasattr(demo_obj, 'ticks') or demo_obj.ticks is None:
        print("Não foi possível encontrar o DataFrame de ticks na demo.")
        return None
    
    print("Colunas disponíveis no DataFrame 'ticks':", demo_obj.ticks.columns)
        
    # Usamos a sintaxe do Polars para obter os nomes únicos e depois remover valores nulos (None)
    jogadores = demo_obj.ticks["name"].unique().drop_nulls().to_list()
    
    if not jogadores:
        print("Nenhum jogador encontrado no DataFrame de ticks.")
        return None

    print("\nJogadores encontrados na partida:")
    for i, nome in enumerate(jogadores):
        print(f"[{i}] - {nome}")

    while True:
        try:
            escolha = int(input("\nDigite o número do jogador que você quer analisar: "))
            if 0 <= escolha < len(jogadores):
                jogador_selecionado = jogadores[escolha]
                print(f"Você selecionou: {jogador_selecionado}")
                return jogador_selecionado
            else:
                print("Número inválido. Por favor, escolha um número da lista.")
        except ValueError:
            print("Entrada inválida. Por favor, digite apenas o número.")
            
def main():
    print("--- INICIANDO ANÁLISE DE DEMO CS ---")
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo 'config.json' não encontrado.")
        return

    dados_partida_obj = parse_demo(config["caminho_demo"])
    if dados_partida_obj is None:
        print("Não foi possível processar a demo. Encerrando.")
        return

    jogador_alvo = selecionar_jogador(dados_partida_obj)
    if not jogador_alvo:
        print("Nenhum jogador selecionado. Encerrando.")
        return

    if config["tipo_analise"] == "posicionamento_jogador":
        posicoes_df = extrair_posicoes_jogador(
            dados_partida_obj,
            [jogador_alvo],
            config["lado"]
        )
        
        if not posicoes_df.empty:
            nome_arquivo = f"{config['nome_mapa']}_{jogador_alvo}_{config['lado']}_heatmap.png"
            caminho_saida = os.path.join(config["caminho_saida_base"], nome_arquivo)
            
            criar_heatmap_posicionamento(
                posicoes_df,
                config["caminho_imagem_mapa"],
                caminho_saida,
                config["nome_mapa"]
            )
    else:
        print(f"Tipo de análise '{config['tipo_analise']}' não suportado.")

    print("--- ANÁLISE CONCLUÍDA ---")

if __name__ == "__main__":
    main()