import numpy as np
import pandas as pd
from math import comb


df = pd.read_csv(
    "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2023-24/gws/gw7.csv"
)
print(df.loc[df["total_points"] > 4, :].sort_values(["total_points"], ascending=False))
df = df.loc[df["total_points"] > 4, :]
print("Total:          {:.3E}".format(comb(df.shape[0], 15)))
n_GK = df.loc[df["position"] == "GK", :].shape[0]
n_DEF = df.loc[df["position"] == "DEF", :].shape[0]
n_MID = df.loc[df["position"] == "MID", :].shape[0]
n_FWD = df.loc[df["position"] == "FWD", :].shape[0]
c_GK = comb(n_GK, 2)
c_DEF = comb(n_DEF, 5)
c_MID = comb(n_MID, 5)
c_FWD = comb(n_FWD, 3)
print("comb(n_GK, 2):  {:.3E}".format(c_GK))
print("comb(n_DEF, 5): {:.3E}".format(c_DEF))
print("comb(n_MID, 5): {:.3E}".format(c_MID))
print("comb(n_FWD, 3): {:.3E}".format(c_FWD))
print("Total (via position): {:.3E}".format(c_GK * c_DEF * c_MID * c_FWD))

### Find approximate proportion of 15 players that meet condition for squad
valid_squads, invalid_squads = 0, 0
ideal_position_counts = pd.DataFrame(
    index=["GK", "DEF", "MID", "FWD"], columns=["count"], data=[2, 5, 5, 3]
)
df_GK = df.loc[df["position"] == "GK", :]
df_DEF = df.loc[df["position"] == "DEF", :]
df_MID = df.loc[df["position"] == "MID", :]
df_FWD = df.loc[df["position"] == "FWD", :]
for i in range(int(1e4)):
    df_squad = pd.concat(
        [df_GK.sample(n=2), df_DEF.sample(n=5), df_MID.sample(n=5), df_FWD.sample(n=3)]
    )
    team_counts = df_squad["team"].value_counts()
    if df_squad["value"].sum(axis=0) > 1000.0:
        invalid_squads += 1
    elif team_counts.max() > 3:
        invalid_squads += 1
    else:
        valid_squads += 1

print("valid_squads: {}".format(valid_squads))
print("invalid_squads: {}".format(invalid_squads))
print("Valid percentage: {}".format(100 * (valid_squads / invalid_squads)))
