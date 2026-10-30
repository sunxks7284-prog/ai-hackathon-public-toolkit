#!/usr/bin/env python3
"""Read-only CSV profiler. Does not modify the source file."""
import argparse
from pathlib import Path
import pandas as pd

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="Input CSV path")
    p.add_argument("--output", default="output/data_profile.txt")
    p.add_argument("--encoding", default=None)
    a = p.parse_args()
    src = Path(a.input)
    if not src.exists():
        raise SystemExit(f"File not found: {src}")
    kw = {"encoding": a.encoding} if a.encoding else {}
    df = pd.read_csv(src, **kw)
    report = [
        f"File: {src}", f"Rows: {len(df)}", f"Columns: {len(df.columns)}",
        "", "Dtypes:", df.dtypes.to_string(),
        "", "Missing:", df.isna().sum().to_string(),
        "", f"Duplicate rows: {int(df.duplicated().sum())}",
        "", "Numeric summary:", df.describe(include="number").to_string(),
        "", "Sample:", df.head().to_string(index=False)
    ]
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    print(f"\nSaved: {out}")

if __name__ == "__main__":
    main()
