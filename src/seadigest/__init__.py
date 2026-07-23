"""seadigest: gooey, liquid-looking seaborn charts over a built-in sample dataset.

Public API — two plotting functions: ``sales_by_category`` and ``sales_over_week``.
"""

from .plots import sales_by_category, sales_over_week

__version__ = "0.1.0"
__all__ = ["sales_by_category", "sales_over_week", "__version__"]
