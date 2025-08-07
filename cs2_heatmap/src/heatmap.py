from awpy.plot import heatmap
from awpy import Demo
import matplotlib.pyplot as plt
import polars as pl

dem = Demo("./demos/mirage_inatel_suns.dem", verbose=True)
dem.parse(player_props=["health", "armor_value", "pitch", "yaw", "round_num"])

# --- PASSO 1: Identificar os times pela lista de jogadores do primeiro round ---

# Filtra os ticks apenas do primeiro round
round_1_ticks = dem.ticks.filter(pl.col("round_num") == 1)

# Pega a lista de nomes únicos de jogadores que estavam no lado CT no round 1
time_A_jogadores = round_1_ticks.filter(pl.col("side") == "ct")["name"].unique().to_list()

# Pega a lista de nomes únicos de jogadores que estavam no lado TR no round 1
time_B_jogadores = round_1_ticks.filter(pl.col("side") == "tr")["name"].unique().to_list()

print("Jogadores inferidos para o 'Time A':", time_A_jogadores)
print("Jogadores inferidos para o 'Time B':", time_B_jogadores)


# --- PASSO 2: Escolher um time e filtrar suas posições de CT em TODA a partida ---

# Vamos analisar o "Time A" (o time que começou de CT)
TIME_ALVO_JOGADORES = time_A_jogadores

# Filtramos TODOS os ticks da partida com duas condições:
# 1. O jogador deve pertencer à lista de jogadores do nosso time alvo.
# 2. O lado do jogador naquele tick deve ser "ct".
posicoes_time_alvo_ct = dem.ticks.filter(
    (pl.col("name").is_in(TIME_ALVO_JOGADORES)) &
    (pl.col("side") == "ct") &
    (pl.col("health") > 0)
)

player_locations = list(
    dem.ticks.filter(pl.col("health") > 0, pl.col("side") == "ct",(pl.col("round_num")))[["X", "Y", "Z"]].sample(100000).iter_rows()
)
fig, ax = heatmap(
    map_name="de_mirage",
    points=player_locations,
    method="kde",
    size=80,
    kde_lower_bound=0.01
)

ax.set_title(f"Mapa de Calor de Posições CT ") 
plt.show()
