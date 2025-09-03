# aggregation.py
import pandas as pd
import numpy as np

def aggregation(df: pd.DataFrame, freq: str):
    agg = df.resample(freq).agg(
        mean=("Hastighed", "mean"),
        size=("Hastighed", "size"),
        std =("Hastighed", "std"),
    )
    agg["hour"] = agg.index.hour
    agg = agg[(agg["hour"] >= 6) & (agg["hour"] <= 18)]
    agg = agg[agg["size"] > 0]
    return agg

def binned_median_iqr(agg: pd.DataFrame, nbins: int = 20):
    """Bin by x='size' and return x (bin center), median(y), q25, q75 where y='mean'."""
    x = agg["size"].to_numpy()
    bins = np.linspace(x.min(), x.max(), nbins + 1)
    k = np.digitize(x, bins, right=False)  # bins 1..nbins
    g = agg.groupby(k, dropna=True)

    x_bin = g["size"].mean()                   # use mean x-position per bin
    y_med = g["mean"].median()
    q25   = g["mean"].quantile(0.25)
    q75   = g["mean"].quantile(0.75)

    return x_bin.values, y_med.values, q25.values, q75.values
