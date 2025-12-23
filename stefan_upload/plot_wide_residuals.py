#!/usr/bin/env python3
"""
plot_wide_residuals.py

Plot wide-format residuals:
- Input CSV columns: time, <field>_init, <field>_final, ...
- Produces a semilog-y plot and saves to PNG.

Usage:
  python plot_wide_residuals.py path/to/residuals_wide.csv [-o residuals.png]
       [-f "p,Ux,Uy,Uz,k,epsilon,omega,T"] [--tmin 0] [--tmax 100] [--no-init] [--no-final]
"""

import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser(description="Plot wide-format OpenFOAM residuals.")
    ap.add_argument("csv", help="Path to *log_residuals_wide.csv")
    ap.add_argument("-o", "--output", default=None, help="Output PNG filename (default: <csv_stem>.png)")
    ap.add_argument("-f", "--fields", default=None,
                    help="Comma-separated list of fields to plot (e.g., 'p,Ux,Uy,Uz,k,epsilon,omega,T'). "
                         "Default: plot all detected fields.")
    ap.add_argument("--tmin", type=float, default=None, help="Minimum time to plot")
    ap.add_argument("--tmax", type=float, default=None, help="Maximum time to plot")
    ap.add_argument("--no-init", action="store_true", help="Do not plot *_init series")
    ap.add_argument("--no-final", action="store_true", help="Do not plot *_final series")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    if "time" not in df.columns:
        raise ValueError("CSV must contain a 'time' column.")

    # Time window
    if args.tmin is not None:
        df = df[df["time"] >= args.tmin]
    if args.tmax is not None:
        df = df[df["time"] <= args.tmax]

    # Detect fields by suffix
    init_cols = [c for c in df.columns if c.endswith("_init")]
    final_cols = [c for c in df.columns if c.endswith("_final")]

    # Base field names (without suffix)
    fields_detected = sorted({c[:-5] for c in init_cols} | {c[:-6] for c in final_cols})

    # Field filter
    if args.fields:
        wanted = [f.strip() for f in args.fields.split(",") if f.strip()]
        fields = [f for f in fields_detected if f in wanted]
    else:
        fields = fields_detected

    if not fields:
        raise ValueError("No fields to plot. Check --fields or CSV column names.")

    # Prepare plot
    plt.figure(figsize=(10, 6))
    for f in fields:
        if not args.no_init:
            col = f + "_init"
            if col in df.columns:
                plt.semilogy(df["time"], df[col], label=f"{f} init")
        #if not args.no_final:
           # col = f + "_final"
           # if col in df.columns:
                #plt.semilogy(df["time"], df[col], label=f"{f} final")

    plt.xlabel("Time")
    plt.ylabel("Residual")
    plt.grid(True, which="both", linestyle=":")
    plt.legend(ncol=2)
    plt.tight_layout()

    out = args.output or (os.path.splitext(os.path.basename(args.csv))[0] + ".png")
    plt.savefig(out, dpi=200)
    print(f"Saved plot to: {out}")

if __name__ == "__main__":
    main()
