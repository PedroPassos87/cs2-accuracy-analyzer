from awpy.plot import heatmap
from awpy import Demo
import matplotlib.pyplot as plt
import polars as pl

dem = Demo("./demos/mirage_inatel_suns.dem", verbose=True)
dem.parse(player_props=["health", "armor_value", "pitch", "yaw", "round_num"])

round_1_ticks = dem.ticks.filter(pl.col("round_num") == 1)
time_A_jogadores = round_1_ticks.filter(pl.col("side") == "ct")["name"].unique().to_list()
time_B_jogadores = round_1_ticks.filter(pl.col("side") == "tr")["name"].unique().to_list()
print("Jogadores inferidos para o 'Time A':", time_A_jogadores)
print("Jogadores inferidos para o 'Time B':", time_B_jogadores)

TIME_ALVO_JOGADORES = time_A_jogadores

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
