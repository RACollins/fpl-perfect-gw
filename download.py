import numpy as np
import pandas as pd
from math import comb


df = pd.read_csv("https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2023-24/gws/gw7.csv")
#print(df.loc[:, ["name", "position", "total_points", "value"]].sort_values(["total_points"], ascending=False))
n_GK = df.loc[df["position"] == "GK", :].shape[0]
n_DEF = df.loc[df["position"] == "DEF", :].shape[0]
n_MID = df.loc[df["position"] == "MID", :].shape[0]
n_FWD = df.loc[df["position"] == "FWD", :].shape[0]
c_GK = comb(n_GK, 2)
c_DEF = comb(n_DEF, 5)
c_MID = comb(n_MID, 5)
c_FWD = comb(n_FWD, 3)
print("comb(n_GK, 2): {:.3E}".format(c_GK))
print("comb(n_DEF, 5): {:.3E}".format(c_DEF))
print("comb(n_MID, 5): {:.3E}".format(c_MID))
print("comb(n_FWD, 3): {:.3E}".format(c_FWD))
print("Total: {:.3E}".format(c_GK*c_DEF*c_MID*c_FWD))
print("Alt Total: {:.3E}".format(comb(804, 15)))