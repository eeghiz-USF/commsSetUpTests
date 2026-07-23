"""Two digestible seaborn visualizations for the built-in sample dataset.

Both functions share a clean, colorblind-friendly style and return the
Matplotlib ``Axes`` so results can be saved, shown, or further customized.
"""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ._data import _sample_data

__all__ = ["sales_by_category", "sales_over_week"]


def sales_by_category(
    data: Optional[pd.DataFrame] = None,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """Horizontal bar chart of total weekly units sold per drink.

    Bars are sorted largest-to-smallest and labelled with their value, so the
    ranking is readable at a glance. Uses the built-in sample data when
    ``data`` is omitted.
    """
    data = _sample_data() if data is None else data
    totals = (
        data.groupby("drink", as_index=False)["units_sold"]
        .sum()
        .sort_values("units_sold", ascending=False)
    )

    sns.set_theme(style="whitegrid")
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=totals,
        x="units_sold",
        y="drink",
        hue="drink",
        palette="crest",
        legend=False,
        ax=ax,
    )
    ax.set_title("Weekly units sold by drink", fontsize=14, weight="bold")
    ax.set_xlabel("Units sold")
    ax.set_ylabel("")
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=10)
    sns.despine(left=True, bottom=True, ax=ax)
    ax.figure.tight_layout()
    return ax


def sales_over_week(
    data: Optional[pd.DataFrame] = None,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """Line chart of daily units sold per drink across the week.

    Each drink is one line with point markers, making trends and the weekend
    spike easy to follow. Uses the built-in sample data when ``data`` is
    omitted.
    """
    data = _sample_data() if data is None else data

    sns.set_theme(style="whitegrid")
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))

    sns.lineplot(
        data=data,
        x="day",
        y="units_sold",
        hue="drink",
        marker="o",
        palette="colorblind",
        ax=ax,
    )
    ax.set_title("Daily sales trend through the week", fontsize=14, weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Units sold")
    ax.legend(title="Drink", bbox_to_anchor=(1.02, 1), loc="upper left")
    sns.despine(ax=ax)
    ax.figure.tight_layout()
    return ax
