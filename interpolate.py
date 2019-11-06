import pandas as pd

df = pd.read_csv("darksky_raw.csv")

print(df)
df = df.interpolate()
df.to_csv('darksky_interp.csv')