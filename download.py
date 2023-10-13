import numpy as np
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2023-24/gws/gw7.csv")
print(df.loc[:, ["name", "position", "total_points", "value"]].sort_values(["total_points"], ascending=False))