#!/usr/bin/env python3
"""
"""

import argparse
import csv
import gzip
import os
import re
from collections import defaultdict, OrderedDict

# Regex patterns for typical OpenFOAM log lines
RE_TIME = re.compile(r'^\s*Time\s*=\s*([0-9Ee+\-\.]+)')
RE_SOLVING = re.compile(r'Solving for\s+([A-Za-z0-9_\.]+)')
RE_SOLVER = re.compile(r'^\s*([A-Za-z0-9_]+):')
RE_INIT = re.compile(r'Initial residual\s*=\s*([0-9Ee+\-\.]+)')
RE_FINAL = re.compile(r'Final residual\s*=\s*([0-9Ee+\-\.]+)')
RE_ITERS = re.compile(r'No Iterations\s*([0-9]+)')
RE_CONT = re.compile(r'^\s*time step continuity errors.*?global\s*=\s*([0-9Ee+\-\.]+).*?cumulative\s*=\s*([0-9Ee+\-\.]+)',
                     re.IGNORECASE)

def open_maybe_gz(path):
    return gzip.open(path, 'rt', encoding='utf-8', errors='replace') if path.endswith('.gz') else open(path, 'r', encoding='utf-8', errors='replace')

def parse_log(log_path):
    """
    """
    residuals_long = []
    continuity = []

    current_time = None

    with open_maybe_gz(log_path) as f:
        for line in f:
            # Time line
            m_time = RE_TIME.match(line)
            if m_time:
                try:
                    current_time = float(m_time.group(1))
                except Exception:
                    current_time = None
                continue

            # Continuity errors
            m_cont = RE_CONT.match(line)
            if m_cont and current_time is not None:
                global_err = m_cont.group(1)
                cumulative_err = m_cont.group(2)
                continuity.append({
                    'time': current_time,
                    'global': global_err,
                    'cumulative': cumulative_err
                })
                continue

            # Residual lines: solver + "Solving for ..."
            if 'Solving for' in line:
                m_field = RE_SOLVING.search(line)
                m_solver = RE_SOLVER.match(line)
                m_init = RE_INIT.search(line)
                m_final = RE_FINAL.search(line)
                m_iters = RE_ITERS.search(line)

                if current_time is None or not m_field or not m_init or not m_final:
                   
                    continue

                field = m_field.group(1)
                init = m_init.group(1)
                final = m_final.group(1)
                iters = m_iters.group(1) if m_iters else ""
                solver = m_solver.group(1) if m_solver else ""

                residuals_long.append({
                    'time': current_time,
                    'field': field,
                    'init': init,
                    'final': final,
                    'iterations': iters,
                    'solver': solver
                })

    return residuals_long, continuity

def write_long_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['time', 'field', 'init', 'final', 'iterations', 'solver'])
        w.writeheader()
        for r in rows:
            w.writerow(r)

def pivot_wide(rows):
    """
    
    """
    # Keep times ordered as encountered
    times = []
    seen_time = set()
    fields = set()

    # data[time] = dict(col -> value)
    data = OrderedDict()

    for r in rows:
        t = r['time']
        if t not in seen_time:
            times.append(t)
            seen_time.add(t)
            data[t] = {}
        field = r['field']
        fields.add(field)
        data[t][f'{field}_init'] = r['init']
       #data[t][f'{field}_final'] = r['final']

    fields = sorted(fields, key=str)  # consistent order
    header = ['time'] + [f'{f}_init' for f in fields] + [f'{f}_final' for f in fields]

    wide_rows = []
    for t in times:
        row = {'time': t}
        for f in fields:
            row[f'{f}_init'] = data[t].get(f'{f}_init', '')
          #row[f'{f}_final'] = data[t].get(f'{f}_final', '')
        wide_rows.append(row)

    return header, wide_rows

def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def main():
    ap = argparse.ArgumentParser(description="Extract residuals from an OpenFOAM log file.")
    ap.add_argument("log", help="Path to solver log (supports .gz)")
    ap.add_argument("-o", "--outdir", default=".", help="Output directory (default: .)")
    ap.add_argument("-p", "--prefix", default=None, help="Output filename prefix (default: derived from log filename)")
    args = ap.parse_args()

    log_base = os.path.basename(args.log)
    stem = os.path.splitext(log_base)[0]
    if stem.endswith('.log'):
        stem = stem[:-4]
    prefix = args.prefix or stem or "openfoam"

    residuals_long, continuity = parse_log(args.log)


    
    header, wide_rows = pivot_wide(residuals_long)
    wide_path = os.path.join(args.outdir, f"{prefix}_residuals.csv")
    write_csv(wide_path, header, wide_rows)

    # Continuity CSV (optional)
    if continuity:
        cont_path = os.path.join(args.outdir, f"{prefix}_continuity.csv")
        write_csv(cont_path, ['time', 'global', 'cumulative'], continuity)

    #print(f"Wrote: {long_path}")
    print(f"Wrote: {wide_path}")
    if continuity:
        print(f"Wrote: {cont_path}")

if __name__ == "__main__":
    main()
