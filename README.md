# seadigest

Digestible, ready-to-read [seaborn](https://seaborn.pydata.org/) visualizations
for a built-in sample dataset. `seadigest` wraps common seaborn plots with
sensible, accessible defaults — sorted bars with value labels, a colorblind-
friendly palette, clean de-spined axes — so you get a clear chart in one call.

## Install

```bash
pip install seadigest
```

## Usage

The package exposes exactly **two functions**, each producing a different
visualization. Call them with no arguments to use the bundled sample dataset
(a week of café drink sales), or pass your own long-form `DataFrame` with
`day`, `drink`, and `units_sold` columns.

```python
import matplotlib.pyplot as plt
import seadigest

# 1. Ranked bar chart: total units sold per drink
seadigest.sales_by_category()

# 2. Trend lines: daily units sold per drink across the week
seadigest.sales_over_week()

plt.show()
```

Both functions return the Matplotlib `Axes`, so you can save or tweak the
result:

```python
ax = seadigest.sales_by_category()
ax.figure.savefig("weekly_sales.png", dpi=150, bbox_inches="tight")
```

### Quick demo

A ready-to-run script is included. After installing the package, run:

```bash
python run_demo.py
```

It draws both charts, saves them as PNGs, and opens them in a window.

### The sample dataset

A small, deterministic dataset is included so the plots work out of the box:

| day | drink      | units_sold |
|-----|------------|------------|
| Mon | Latte      | 40         |
| ... | ...        | ...        |
| Sat | Latte      | 64         |

## API

| Function | Visualization |
|----------|---------------|
| `sales_by_category(data=None, ax=None)` | Horizontal bar chart of total weekly units per drink, sorted and value-labelled. |
| `sales_over_week(data=None, ax=None)`   | Line chart of daily units sold per drink across the week. |

## Development

```bash
python -m build                 # build sdist + wheel
python -m twine upload dist/*   # publish to PyPI
```

## License

MIT
