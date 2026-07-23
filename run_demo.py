"""run_demo.py — a runnable demo of the `seadigest` package.

Run it from the project folder after installing the package:

    pip install -e .
    python run_demo.py

It calls both of seadigest's plotting functions on the built-in sample
dataset, saves each chart to a PNG next to this file, and opens them in a
window (close the windows to exit).
"""

import matplotlib.pyplot as plt

try:
    import seadigest
except ModuleNotFoundError:
    raise SystemExit(
        "seadigest isn't installed yet.\n"
        "From this folder run:\n"
        "    pip install -e .\n"
        "then try again:\n"
        "    python run_demo.py"
    )


def main() -> None:
    print(f"seadigest version {seadigest.__version__}")
    print("Building charts from the built-in sample dataset...\n")

    # 1. Ranked bar chart: total units sold per drink.
    ax_bar = seadigest.sales_by_category()
    ax_bar.figure.savefig("sales_by_category.png", dpi=150, bbox_inches="tight")
    print("  saved sales_by_category.png")

    # 2. Trend lines: daily units sold per drink across the week.
    ax_line = seadigest.sales_over_week()
    ax_line.figure.savefig("sales_over_week.png", dpi=150, bbox_inches="tight")
    print("  saved sales_over_week.png")

    print("\nOpening chart windows — close them to exit.")
    plt.show()


if __name__ == "__main__":
    main()
