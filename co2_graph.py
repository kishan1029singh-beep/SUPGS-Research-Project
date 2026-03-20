##!/usr/bin/env python3
"""
co2_graph.py

Improved example script to compare CO2 growth with/without SUPGS model.
Features:
- argparse for parameters
- optional CSV input (vehicles, co2)
- configurable reduction percent (default 12%)
- save plot to file or show interactively
- simple linear/exponential model for baseline if CSV not provided
Author: Kishan Singh (improved)
"""

import argparse
import math
from typing import List, Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np
import csv
import os

try:
    import pandas as pd
except Exception:
    pd = None  # pandas optional; fallback to csv module


def generate_baseline(vehicles: List[float], model: str = "linear") -> List[float]:
    """Generate a simple baseline CO2 series from vehicles.
    model: 'linear' or 'exp' (exponential)
    """
    if model == "exp":
        # exponential growth approx: co2 = a * exp(b * vehicles_index)
        a = 15.0
        b = 0.12
        return [a * math.exp(b * i) for i in range(len(vehicles))]
    # default linear mapping (scale factor)
    scale = 1.6
    return [v * scale for v in vehicles]


def apply_supgs_reduction(baseline: List[float], reduction_percent: float) -> List[float]:
    """Apply a percentage reduction to baseline CO2 values."""
    factor = max(0.0, 1.0 - reduction_percent / 100.0)
    return [c * factor for c in baseline]


def read_csv_data(path: str) -> Tuple[List[float], List[float]]:
    """Read CSV with columns 'vehicles' and 'co2' (or first two columns)."""
    if pd:
        df = pd.read_csv(path)
        if "vehicles" in df.columns and "co2" in df.columns:
            return df["vehicles"].tolist(), df["co2"].tolist()
        # fallback: take first two numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            return df[numeric_cols[0]].tolist(), df[numeric_cols[1]].tolist()
        raise ValueError("CSV does not contain usable numeric columns")
    # fallback without pandas
    vehicles = []
    co2 = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        for row in reader:
            if not row:
                continue
            try:
                v = float(row[0])
                c = float(row[1])
            except Exception:
                continue
            vehicles.append(v)
            co2.append(c)
    if not vehicles or not co2:
        raise ValueError("CSV reading failed or no numeric data found")
    return vehicles, co2


def plot_series(vehicles, baseline, with_supgs, title: str, save_path: Optional[str], show_plot: bool):
    plt.figure(figsize=(8, 5))
    plt.plot(vehicles, baseline, marker="o", label="Without Green System")
    plt.plot(vehicles, with_supgs, marker="o", label="With SUPGS Model")
    plt.xlabel("Vehicle Growth (index or count)")
    plt.ylabel("CO2 Level (relative units)")
    plt.title(title)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        plt.savefig(save_path, dpi=200)
        print(f"Saved plot to {save_path}")
    if show_plot:
        plt.show()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="SUPGS CO2 comparison plot")
    parser.add_argument("--input", "-i", help="Optional CSV input path (vehicles,co2)")
    parser.add_argument("--reduction", "-r", type=float, default=12.0,
                        help="Reduction percent applied by SUPGS (default 12.0)")
    parser.add_argument("--model", "-m", choices=["linear", "exp"], default="linear",
                        help="Baseline model if CSV not provided")
    parser.add_argument("--save", "-s", help="Save plot to file (e.g., out.png)")
    parser.add_argument("--no-show", action="store_true", help="Do not show interactive plot")
    args = parser.parse_args()

    if args.input:
        vehicles, baseline = read_csv_data(args.input)
    else:
        # sample synthetic data (vehicle counts)
        vehicles = [10, 20, 30, 40, 50, 60]
        baseline = generate_baseline(vehicles, model=args.model)

    with_supgs = apply_supgs_reduction(baseline, args.reduction)

    title = f"CO2 Reduction using SUPGS Model (reduction={args.reduction}%)"
    plot_series(vehicles, baseline, with_supgs, title, args.save, not args.no_show)


if __name__ == "__main__":
    main()
