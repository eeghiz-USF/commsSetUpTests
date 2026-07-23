"""seadigest: digestible seaborn visualizations for a built-in sample dataset.

Public API — exactly two plotting functions:

    >>> import seadigest
    >>> seadigest.sales_by_category()   # ranked bar chart
    >>> seadigest.sales_over_week()     # weekly trend lines
"""

from .plots import sales_by_category, sales_over_week

__version__ = "0.1.0"
__all__ = ["sales_by_category", "sales_over_week", "__version__"]
