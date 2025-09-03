import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
from matplotlib import gridspec
import numpy as np 
from statsmodels.nonparametric.smoothers_lowess import lowess
from typing import Sequence, Tuple
from aggregation import aggregation
from labels import time_of_day_label, COLORS

def plot_fordelings_af_hastigheder(df: pd.DataFrame, metadata): 
    """Plot der viser fordeling af hastigheder gennem Histogram, boxplot og violinplot.
    De tre plots illustrerer samme data på forskellige måder.
    """
    sns.set_style("whitegrid")

    # Data
    data = df["Hastighed"].dropna()
    
    # --- Samlet figurtekst nederst ---
    sitename = metadata.get("Sitename", "Ukendt sted")
    min_date = metadata.get("min-date", "Ukendt dato")
    max_date = metadata.get("max-date", "Ukendt dato")

    # Figur + grid
    fig = plt.figure(figsize=(12, 10))
    grid = gridspec.GridSpec(2, 2, height_ratios=[4, 2], hspace=0.45, wspace=0.25)

    # --- Samlet figurtekst nederst ---
    sitename = metadata.get("Sitename", "Ukendt sted")
    min_date = metadata.get("min-date", "Ukendt dato")
    max_date = metadata.get("max-date", "Ukendt dato")

    # --- Histogram (øverst, begge kolonner) ---
    ax_hist = fig.add_subplot(grid[0, :])
    ax_hist.hist(data, bins=25, edgecolor="black", color="salmon")
    ax_hist.set_xlabel("Hastighed (km/t)")
    ax_hist.set_ylabel("Antal cykler")
    ax_hist.set_title(f"Fordeling af cykelhastigheder for {sitename}", fontsize=16)

    # Markér middel & median
    mean = data.mean()
    median = data.median()
    ax_hist.axvline(mean,   linestyle="--", linewidth=1.2, color="k", label=f"Middel: {mean:.1f}")
    ax_hist.axvline(median, linestyle=":",  linewidth=1.2, color="k", label=f"Median: {median:.1f}")
    ax_hist.legend(frameon=True)

    # Ens x-limits på alle tre plots
    xmin, xmax = np.floor(data.min()) - 2, np.ceil(data.max()) + 2

    # --- Boxplot (nederst til venstre) ---
    ax_box = fig.add_subplot(grid[1, 0])
    sns.boxplot(x=data, ax=ax_box, color="skyblue")
    ax_box.set_xlabel("Hastighed (km/t)")
    ax_box.set_yticks([])
    ax_box.set_xlim(xmin, xmax)
    sns.despine(ax=ax_box, left=True)

    # --- Violinplot (nederst til højre) ---
    ax_violin = fig.add_subplot(grid[1, 1])
    sns.violinplot(x=data, ax=ax_violin, inner="box", color="lightgreen")
    ax_violin.set_xlabel("Hastighed (km/t)")
    ax_violin.set_yticks([])
    ax_violin.set_xlim(xmin, xmax)
    sns.despine(ax=ax_violin, left=True)


    fig.text(
        0.1, -0.001, 
        f"Figuren viser fordelingen af cykelhastigheder som histogram, boxplot og violinplot.\n"
        f"Histogrammet viser antallet af cykler i intervaller af hastighed, boxplottet opsummerer\n"
        f"median, kvartiler og outliers, mens violinplottet viser fordelingens form.\n"
        f"Data er indsamlet ved {sitename} i perioden {min_date} til {max_date}.",
        ha="left", va="top", fontsize=10, color="grey", alpha=0.8
    )

    plt.show()
    # plotting.py
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from typing import Sequence, Tuple

from aggregation import aggregation, binned_median_iqr
from labels import time_of_day_label, COLORS
from config import NBINS

def plot_scatter_lowess_panels(df,
                               freqs: Sequence[Tuple[str, float, str]],
                               figsize=(15, 5)):
    fig, axes = plt.subplots(1, len(freqs), figsize=figsize)

    if len(freqs) == 1:
        axes = [axes]

    for ax, (freq, frac, title) in zip(np.ravel(axes), freqs):
        agg = aggregation(df, freq)

        # scatter (colored by time of day)
        labels = agg["hour"].apply(time_of_day_label)
        for label, color in COLORS.items():
            m = labels == label
            if m.any():
                ax.scatter(
                    agg.loc[m, "size"], agg.loc[m, "mean"],
                    s=10, alpha=0.35, color=color, label=label
                )

        # LOWESS line
        if len(agg) >= 5:
            sm = lowess(agg["mean"], agg["size"], frac=frac, return_sorted=True)
            ax.plot(sm[:, 0], sm[:, 1], linewidth=2, color="black", label="LOWESS")

        # ----- Binned IQR ribbon (median not drawn; ribbon shows variability) -----
        xb, ymed, q25, q75 = binned_median_iqr(agg, nbins=NBINS)
        if len(xb) > 1:
            order = np.argsort(xb)
            xb, q25, q75 = xb[order], q25[order], q75[order]
            ax.fill_between(xb, q25, q75, color="black", alpha=0.15, label="IQR (25–75%)")

        # axes styling
        ax.set_title(title)
        ax.set_xlabel(f"Flow (cykler/{freq})")
        ax.set_ylabel("Gennemsnits hastigheden (km/t)")
        ax.minorticks_on()
        ax.grid(True, which="major", linestyle="-", linewidth=0.3, color="black", alpha=0.4)
        ax.grid(True, which="minor", linestyle=":", linewidth=0.5, color="grey", alpha=0.2)

    axes[0].set_ylabel("Hastighed (km/t)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc="upper center", bbox_to_anchor=(0.5, -0.05),
        frameon=True, fancybox=True, title="Time of day",
        ncol=4
    )
    fig.tight_layout(rect=[0.05, 0.05, 0.98, 0.9])
    return fig, axes
