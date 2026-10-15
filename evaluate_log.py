"""
Builds confusion tables from ripeness_log.csv (made by tomato_ripeness.py).

Run:
    python evaluate_log.py
    python evaluate_log.py path/to/other_log.csv

Rows are the TRUE label you pressed (1/2/3), columns are what the program predicted.
White balance ON and OFF are reported separately so you can compare them.
"""

import csv
import sys

import numpy as np

LABELS = ["NOT YET", "ALMOST", "RIPE"]


def confusion(rows):
    matrix = np.zeros((3, 3), dtype=int)
    for r in rows:
        true_label, predicted = r["true_label"], r["predicted"]
        if true_label in LABELS and predicted in LABELS:
            matrix[LABELS.index(true_label), LABELS.index(predicted)] += 1
    return matrix


def show(title, matrix):
    print(f"\n{title}  (rows = true, columns = predicted)")
    print("".ljust(10) + "".join(label.ljust(10) for label in LABELS))
    for i, label in enumerate(LABELS):
        print(label.ljust(10) + "".join(str(v).ljust(10) for v in matrix[i]))
    total = matrix.sum()
    if total == 0:
        print("No usable rows.")
        return
    correct = np.trace(matrix)
    print(f"Accuracy: {correct / total * 100:.1f}%  ({correct}/{total})")
    for i, label in enumerate(LABELS):
        n = matrix[i].sum()
        if n:
            print(f"  {label} recall: {matrix[i, i] / n * 100:.1f}%  ({matrix[i, i]}/{n})")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "ripeness_log.csv"
    try:
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Could not find {path}. Log some readings with keys 1/2/3 first.")
        return

    if not rows:
        print("The log file has no rows yet.")
        return

    show("ALL READINGS", confusion(rows))
    for flag in ("on", "off"):
        subset = [r for r in rows if r["white_balance"] == flag]
        if subset:
            show(f"WHITE BALANCE {flag.upper()}", confusion(subset))


if __name__ == "__main__":
    main()