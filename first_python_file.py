import numpy as np
import pandas as pd

df = pd.DataFrame(
    index=["a", "b", "c"],
    columns=["A", "B", "C", "D", "E", "F", "G"],
    data=np.random.random(21).reshape(3, 7),
)

print(df)
