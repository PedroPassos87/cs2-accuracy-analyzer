from awpy.plot import heatmap
from awpy import Demo
from tqdm import tqdm
import polars as pl

dem = Demo("./demos/mirage_inatel_suns.dem", verbose=True)
dem.parse(player_props=["health", "armor_value", "pitch", "yaw"])

player_locations = list(
    dem.ticks.filter(pl.col("health") > 0, pl.col("side") == "ct")[["X", "Y", "Z"]].sample(100000).iter_rows()
)
fig, ax = heatmap(
    map_name="de_mirage",
    points=player_locations,
    method="kde",
    size=80,
    kde_lower_bound=0.01
)
