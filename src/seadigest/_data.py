"""Built-in sample dataset used by the seadigest plotting functions."""

from __future__ import annotations

import pandas as pd

# Days of the week in display order.
_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Typical weekday demand pattern (quiet midweek, busy weekend).
_WEEKDAY_FACTOR = [1.00, 0.90, 0.95, 1.05, 1.30, 1.60, 1.20]

# Baseline daily units for each drink on the menu.
_BASELINE = {
    "Latte": 40,
    "Cappuccino": 32,
    "Espresso": 25,
    "Mocha": 20,
    "Green Tea": 15,
}


def _sample_data() -> pd.DataFrame:
    """Return a small, deterministic café-sales dataset in long form.

    Columns:
        day        ordered categorical, Mon..Sun
        drink      the menu item
        units_sold integer units sold that day
    """
    rows = [
        {"day": day, "drink": drink, "units_sold": round(base * factor)}
        for drink, base in _BASELINE.items()
        for day, factor in zip(_DAYS, _WEEKDAY_FACTOR)
    ]
    frame = pd.DataFrame(rows)
    frame["day"] = pd.Categorical(frame["day"], categories=_DAYS, ordered=True)
    return frame
