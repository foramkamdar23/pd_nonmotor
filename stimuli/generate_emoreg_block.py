#!/usr/bin/env python3
"""
generate_emoreg_block.py

Creates a fixed, balanced stimulus manifest CSV for the Emotion Regulation task.

Balance constraints (hard):
- N_TRIALS total
- N_BINS valence bins
- 2 conditions: FEEL and TONE
- Equal images per bin
- Equal images per bin per condition

Soft objective:
- Try to spread categories within each bin if possible (won't fail if not)

Output CSV columns:
trial,stim_id,filename,category,valence,val_bin,condition
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd

VALENCE_BINS_8 = [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9)]  # last bin inclusive on 9

def assign_val_bin(v: float, bins):
    # bins are list of (low, high) with high exclusive except last
    for i, (lo, hi) in enumerate(bins, start=1):
        if i < len(bins):
            if (v >= lo) and (v < hi):
                return i
        else:
            # last bin includes high endpoint
            if (v >= lo) and (v <= hi):
                return i
    return None

def pick_with_soft_category_balance(df_bin, k, rng):
    """
    Pick k rows from df_bin trying to avoid overusing one category.
    Strategy:
      - repeatedly pick from the currently least-used category among what's available
      - fallback to random if needed
    """
    if k <= 0:
        return df_bin.iloc[0:0]

    # If no category column, just random sample
    if "Category" not in df_bin.columns:
        return df_bin.sample(n=k, random_state=int(rng.integers(0, 2**31-1)))

    remaining = df_bin.copy()
    chosen = []
    cat_counts = {}

    while len(chosen) < k and len(remaining) > 0:
        # compute available categories and their current chosen counts
        cats = remaining["Category"].unique().tolist()
        if not cats:
            break
        cats_sorted = sorted(cats, key=lambda c: cat_counts.get(c, 0))
        # choose from least-used category
        target_cat = cats_sorted[0]
        pool = remaining[remaining["Category"] == target_cat]
        if len(pool) == 0:
            # fallback: random from remaining
            row = remaining.sample(n=1, random_state=int(rng.integers(0, 2**31-1))).iloc[0]
        else:
            row = pool.sample(n=1, random_state=int(rng.integers(0, 2**31-1))).iloc[0]

        chosen.append(row)
        cat_counts[row["Category"]] = cat_counts.get(row["Category"], 0) + 1

        # drop chosen row from remaining by index
        remaining = remaining.drop(index=row.name)

    if len(chosen) < k:
        raise ValueError(f"Could only pick {len(chosen)} images but needed {k} from this bin (insufficient pool).")

    return pd.DataFrame(chosen)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratings_csv", required=True, help="CSV with columns including ID (or Filename), Valence, Category")
    ap.add_argument("--out_csv", required=True, help="Output manifest CSV path")
    ap.add_argument("--n_trials", type=int, default=96)
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--bins", type=str, default="8", help="Currently supports '8' for 1-2..8-9")
    ap.add_argument("--id_col", type=str, default="ID", help="Column containing image id (without .jpg) or filename stem")
    ap.add_argument("--val_col", type=str, default="Valence", help="Valence column name")
    ap.add_argument("--cat_col", type=str, default="Category", help="Category column name")
    ap.add_argument("--ext", type=str, default=".jpg", help="File extension for stimuli")
    args = ap.parse_args()

    if args.bins != "8":
        print("Only --bins 8 is supported right now.", file=sys.stderr)
        sys.exit(1)

    bins = VALENCE_BINS_8
    rng = np.random.default_rng(args.seed)

    df = pd.read_csv(args.ratings_csv)

    # Normalize columns
    if args.id_col not in df.columns:
        raise ValueError(f"Missing id_col '{args.id_col}' in CSV. Columns: {list(df.columns)}")
    if args.val_col not in df.columns:
        raise ValueError(f"Missing val_col '{args.val_col}' in CSV. Columns: {list(df.columns)}")

    # Optional category
    if args.cat_col in df.columns and "Category" != args.cat_col:
        df["Category"] = df[args.cat_col]
    elif "Category" not in df.columns and args.cat_col in df.columns:
        df["Category"] = df[args.cat_col]

    df["stim_id"] = df[args.id_col].astype(str).str.strip()
    df["valence"] = pd.to_numeric(df[args.val_col], errors="coerce")

    df = df.dropna(subset=["valence"]).copy()
    df["val_bin"] = df["valence"].apply(lambda v: assign_val_bin(v, bins))

    df = df.dropna(subset=["val_bin"]).copy()
    df["val_bin"] = df["val_bin"].astype(int)

    n_bins = len(bins)
    if args.n_trials % n_bins != 0:
        raise ValueError(f"n_trials={args.n_trials} must be divisible by n_bins={n_bins} for equal bin counts.")

    per_bin = args.n_trials // n_bins
    if per_bin % 2 != 0:
        raise ValueError(f"per_bin={per_bin} must be even to split equally across FEEL/TONE.")

    per_bin_per_cond = per_bin // 2

    # Feasibility check
    bin_counts = df.groupby("val_bin").size().to_dict()
    for b in range(1, n_bins+1):
        have = bin_counts.get(b, 0)
        if have < per_bin:
            raise ValueError(f"Bin {b} has only {have} images, but need {per_bin}. Adjust n_trials or binning.")

    # Select images bin-by-bin with soft category balance
    selected = []
    for b in range(1, n_bins+1):
        df_bin = df[df["val_bin"] == b]
        picked = pick_with_soft_category_balance(df_bin, per_bin, rng)
        selected.append(picked)

    selected = pd.concat(selected, ignore_index=True)

    # Assign conditions balanced within each bin
    selected["condition"] = None
    for b in range(1, n_bins+1):
        idx = selected.index[selected["val_bin"] == b].to_numpy()
        rng.shuffle(idx)
        feel_idx = idx[:per_bin_per_cond]
        tone_idx = idx[per_bin_per_cond:]
        selected.loc[feel_idx, "condition"] = "FEEL"
        selected.loc[tone_idx, "condition"] = "TONE"

    # Create filename (stem + ext)
    selected["filename"] = selected["stim_id"] + args.ext

    # Randomize overall trial order but keep fixed with seed
    selected = selected.sample(frac=1, random_state=args.seed).reset_index(drop=True)
    selected.insert(0, "trial", np.arange(1, len(selected) + 1))

    # Keep useful columns (category optional)
    out_cols = ["trial", "stim_id", "filename", "Category", "valence", "val_bin", "condition"]
    for c in out_cols:
        if c not in selected.columns:
            selected[c] = ""
    out = selected[out_cols].rename(columns={"Category": "category"})

    os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
    out.to_csv(args.out_csv, index=False)

    # Print summary
    print(f"Wrote: {args.out_csv}")
    print(f"Trials: {len(out)}")
    print("Counts per bin:")
    print(out.groupby("val_bin").size())
    print("Counts per condition:")
    print(out["condition"].value_counts())
    print("Counts per bin x condition:")
    print(out.groupby(["val_bin","condition"]).size().unstack(fill_value=0))

if __name__ == "__main__":
    main()