import json
import numpy
import pandas as pd

data_input = "/home/pi/crystal-imaging/crystal_output.json"
raw_lengths = []
with open(data_input) as crystal_output:
	data = json.load(crystal_output)
	for i in range(len(data)):
		raw_lengths.append(data[i]["length_mm"])
lengths = pd.Series(raw_lengths).sort_values().reset_index(drop=True)
print(lengths)
d10, d50, d90 = lengths.quantile(0.10), lengths.median(), lengths.quantile(0.90)

stats = pd.Series(
    {
        "Min": lengths.min(),
        "Max": lengths.max(),
        "Range": lengths.max() - lengths.min(),
        "Mean": lengths.mean(),
        "Std Dev": lengths.std(),
        "CV (%)": (lengths.std() / lengths.mean()) * 100,
        "d10": d10,
        "d50 (Median)": d50,
        "d90": d90,
        "Span": (d90 - d10) / d50 if d50 != 0 else None,
    }
)


stats.to_csv("population_stats.csv", header=["Value"])
