import numpy as np
import pandas as pd


def knapSack(W, wt, val):
    n = len(val)
    table = [[0 for x in range(W + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for j in range(W + 1):
            if i == 0 or j == 0:
                table[i][j] = 0
            elif wt[i - 1] <= j:
                table[i][j] = max(
                    val[i - 1] + table[i - 1][j - wt[i - 1]], table[i - 1][j]
                )
            else:
                table[i][j] = table[i - 1][j]

    return pd.DataFrame(table)


val = [5, 10, 15, 20]
wt = [1, 2, 4, 5]
W = 8

print(knapSack(W, wt, val))
