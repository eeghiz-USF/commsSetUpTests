"""Two gooey, liquid-looking seaborn visualizations for the sample dataset.

Both share a glossy dark style and return the Matplotlib ``Axes``.
"""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from ._data import _sample_data
from ._gooey import catmull_rom, gooey_capsule, liquid_fill, soft_glow

__all__ = ["sales_by_category", "sales_over_week"]

_BG, _INK, _GRID = "#0e1726", "#c9d5e3", "#233145"  # backdrop, text, grid


def _axes(ax, figsize, title):
    """Create (if needed) and apply the shared dark, glossy style to an Axes."""
    sns.set_theme(style="white")
    if ax is None:
        _, ax = plt.subplots(figsize=figsize)
    ax.figure.set_facecolor(_BG)
    ax.set_facecolor(_BG)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=_INK, labelsize=10, length=0)
    ax.set_title(title, color="white", fontsize=15, weight="bold", pad=14)
    ax.set_axisbelow(True)
    return ax


def sales_by_category(data: Optional[pd.DataFrame] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """Ranked bar chart drawn as glossy, gooey gel capsules (one per drink)."""
    data = _sample_data() if data is None else data
    totals = (data.groupby("drink", as_index=False)["units_sold"].sum()
              .sort_values("units_sold", ascending=False).reset_index(drop=True))
    ax = _axes(ax, (9, 5.5), "Weekly units sold by drink")
    n = len(totals)
    palette = sns.color_palette("mako", n_colors=n)
    top = totals["units_sold"].max()
    for i, row in totals.iterrows():
        y = n - 1 - i  # largest capsule on top
        gooey_capsule(ax, row["units_sold"], y, palette[i], thickness=30, zorder=3)
        ax.text(row["units_sold"] + top * 0.02, y, f"{int(row['units_sold'])}",
                va="center", ha="left", color="white", fontsize=11,
                fontweight="bold", zorder=6)
    ax.grid(axis="x", color=_GRID, linewidth=0.8)
    ax.set_yticks(range(n))
    ax.set_yticklabels(list(totals["drink"])[::-1])
    ax.set_xlabel("Units sold", color=_INK)
    ax.set_xlim(0, top * 1.15)
    ax.set_ylim(-0.7, n - 0.3)
    ax.figure.tight_layout()
    return ax


def sales_over_week(data: Optional[pd.DataFrame] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """Weekly trend drawn as smooth liquid streams with a glossy pour beneath."""
    data = _sample_data() if data is None else data
    ax = _axes(ax, (9.5, 5.5), "Daily sales trend through the week")
    col = data["day"]
    days = list(col.cat.categories) if hasattr(col, "cat") else list(dict.fromkeys(col))
    xpos = {d: i for i, d in enumerate(days)}
    drinks = list(dict.fromkeys(data["drink"]))
    palette = sns.color_palette("mako", n_colors=len(drinks))
    top = data["units_sold"].max()
    for color, drink in zip(palette, drinks):
        sub = data[data["drink"] == drink]
        x = np.array([xpos[d] for d in sub["day"]], float)
        y = sub["units_sold"].to_numpy(float)
        order = np.argsort(x)
        x, y = x[order], y[order]
        sx, sy = catmull_rom(x, y)
        liquid_fill(ax, sx, sy, color, base=0, zorder=1)
        soft_glow(ax, sx, sy, color, width=4, zorder=2)
        ax.plot(sx, sy, color=color, lw=4, solid_capstyle="round", zorder=3, label=drink)
        ax.scatter(x, y, s=110, color=color, edgecolor="white", linewidth=1.3, zorder=4)
        ax.scatter(x - 0.05, y + top * 0.02, s=16, color="white", alpha=0.75, zorder=5)
    ax.grid(axis="y", color=_GRID, linewidth=0.8)
    ax.set_xticks(range(len(days)))
    ax.set_xticklabels(days)
    ax.set_ylabel("Units sold", color=_INK)
    ax.set_xlim(-0.3, len(days) - 0.7)
    ax.set_ylim(0, top * 1.18)
    legend = ax.legend(title="Drink", frameon=False, labelcolor=_INK,
                       bbox_to_anchor=(1.02, 1), loc="upper left")
    legend.get_title().set_color(_INK)
    ax.figure.tight_layout()
    return ax
