from awpy.demo import Demo

def parse_demo(caminho_demo: str) -> Demo | None:
    print(f"Iniciando o parse da demo: {caminho_demo}...")
    try:
        demo_obj = Demo(path=caminho_demo, verbose=False)
        print("Objeto Demo criado com sucesso!")
        return demo_obj
    except Exception as e:
        print(f"Ocorreu um erro ao carregar a demo: {e}")
        return None