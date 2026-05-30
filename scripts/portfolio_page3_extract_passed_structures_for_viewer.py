#!/usr/bin/env python3
"""
Extract final-pass PD-L1 mini-binder complex PDBs for portfolio viewing.

Expected runner layout:

data/results/param_sensitivity/{condition_id}/esmfold_predictions/
    validation_results.csv
    esmfold_binder_predictions.csv

The script:
1. Scans all condition folders.
2. Loads validation_results.csv.
3. Keeps designs with mean_plddt >= 80 and rmsd <= 2.0.
4. Copies the corresponding designed_pdb files into viewer_structures/passed_31/.
5. Writes manifest.csv and manifest.json.

Important:
- copied PDBs are RFdiffusion binder-target complex geometries
- binder sequence comes from ProteinMPNN / ESMFold metadata
- these are not relaxed structures
"""

from pathlib import Path
import shutil
import json
import re
import pandas as pd


PROJECT_DIR = Path("/Users/harshadghodke/AIML/pdl1-mini-binder-design")
STUDY_DIR = PROJECT_DIR / "data" / "results" / "param_sensitivity"

OUT_DIR = PROJECT_DIR / "viewer_structures" / "passed_31"

PLDDT_MIN = 80.0
RMSD_MAX = 2.0


def safe_name(text):
    text = str(text)
    text = text.replace("/", "_").replace("\\", "_")
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    return text.strip("_")


def parse_condition(condition_id):
    condition_id = str(condition_id)

    length_match = re.search(r"len(\d+)", condition_id)
    hotspot_match = re.search(r"_(clusterA|clusterB|distributed)_", condition_id)
    noise_match = re.search(r"noise(05|0)", condition_id)

    length = int(length_match.group(1)) if length_match else None
    hotspot = hotspot_match.group(1) if hotspot_match else None
    noise = 0.5 if noise_match and noise_match.group(1) == "05" else 0.0

    return length, hotspot, noise


def resolve_path(path_like):
    if pd.isna(path_like):
        return None

    p = Path(str(path_like))

    if p.exists():
        return p

    # Try relative to project root
    p2 = PROJECT_DIR / p
    if p2.exists():
        return p2

    return None


def load_condition_validation(condition_dir):
    """
    Load validation_results.csv for one condition and recover binder_sequence
    from esmfold_binder_predictions.csv if needed.
    """
    condition_id = condition_dir.name
    esm_dir = condition_dir / "esmfold_predictions"
    val_csv = esm_dir / "validation_results.csv"

    if not val_csv.exists():
        return None

    df_val = pd.read_csv(val_csv)

    if len(df_val) == 0:
        return None

    df_val["condition_id"] = condition_id

    pred_csv = esm_dir / "esmfold_binder_predictions.csv"

    if pred_csv.exists():
        df_pred = pd.read_csv(pred_csv)

        keep_cols = [
            c for c in [
                "condition_id",
                "seq_id",
                "backbone",
                "binder_sequence",
                "binder_length",
                "mean_plddt",
            ]
            if c in df_pred.columns
        ]

        merge_keys = [
            c for c in ["condition_id", "seq_id", "backbone"]
            if c in df_val.columns and c in df_pred.columns
        ]

        if "binder_sequence" not in df_val.columns and "binder_sequence" in df_pred.columns:
            df_val = df_val.merge(
                df_pred[keep_cols].drop_duplicates(),
                on=merge_keys,
                how="left",
                suffixes=("", "_pred"),
            )

    return df_val


def main():
    if not STUDY_DIR.exists():
        raise FileNotFoundError(f"STUDY_DIR does not exist: {STUDY_DIR}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    condition_dirs = sorted([p for p in STUDY_DIR.iterdir() if p.is_dir()])

    print(f"Scanning condition folders under:")
    print(f"  {STUDY_DIR}")
    print(f"Found {len(condition_dirs)} condition folders")

    dfs = []

    for condition_dir in condition_dirs:
        df = load_condition_validation(condition_dir)
        if df is None:
            print(f"  {condition_dir.name}: no validation results")
            continue

        print(f"  {condition_dir.name}: {len(df)} validation rows")
        dfs.append(df)

    if not dfs:
        raise RuntimeError("No validation_results.csv files were loaded.")

    df_all = pd.concat(dfs, ignore_index=True)

    required = ["condition_id", "seq_id", "designed_pdb", "mean_plddt", "rmsd"]
    missing = [c for c in required if c not in df_all.columns]

    if missing:
        raise RuntimeError(f"Missing required columns in validation data: {missing}")

    df_all["passes_final_filter"] = (
        (df_all["mean_plddt"] >= PLDDT_MIN)
        & (df_all["rmsd"] <= RMSD_MAX)
    )

    df_pass = df_all[df_all["passes_final_filter"]].copy()

    print("\nSummary:")
    print(f"  Total validation rows: {len(df_all)}")
    print(f"  Final-pass rows:       {len(df_pass)}")

    if len(df_pass) == 0:
        raise RuntimeError("No final-pass rows found.")

    # Sort by RMSD first, then pLDDT descending
    df_pass = df_pass.sort_values(
        by=["rmsd", "mean_plddt"],
        ascending=[True, False],
    ).reset_index(drop=True)

    manifest = []
    missing_pdbs = []

    for i, row in df_pass.iterrows():
        rank = i + 1

        condition_id = row["condition_id"]
        seq_id = row["seq_id"]
        backbone = row["backbone"] if "backbone" in row and pd.notna(row["backbone"]) else seq_id

        src_pdb = resolve_path(row["designed_pdb"])

        if src_pdb is None:
            missing_pdbs.append({
                "rank": rank,
                "condition_id": condition_id,
                "seq_id": seq_id,
                "designed_pdb": row["designed_pdb"],
            })
            continue

        length, hotspot, noise = parse_condition(condition_id)

        out_name = f"{rank:02d}_{safe_name(condition_id)}__{safe_name(seq_id)}.pdb"
        dst_pdb = OUT_DIR / out_name

        shutil.copy2(src_pdb, dst_pdb)

        manifest_row = {
            "rank": rank,
            "condition_id": condition_id,
            "seq_id": seq_id,
            "backbone": backbone,
            "length": length,
            "hotspot_config": hotspot,
            "noise": noise,
            "pdb_file": out_name,
            "pdb_relpath": str(dst_pdb.relative_to(PROJECT_DIR)),
            "mean_plddt": float(row["mean_plddt"]),
            "rmsd": float(row["rmsd"]),
            "mpnn_score": float(row["mpnn_score"]) if "mpnn_score" in row and pd.notna(row["mpnn_score"]) else None,
            "global_score": float(row["global_score"]) if "global_score" in row and pd.notna(row["global_score"]) else None,
            "binder_sequence": str(row["binder_sequence"]) if "binder_sequence" in row and pd.notna(row["binder_sequence"]) else None,
            "source_designed_pdb": str(src_pdb),
        }

        manifest.append(manifest_row)

    if missing_pdbs:
        missing_df = pd.DataFrame(missing_pdbs)
        missing_df.to_csv(OUT_DIR / "missing_pdbs.csv", index=False)
        print(f"\nWARNING: Missing source PDBs: {len(missing_df)}")
        print(f"Wrote: {OUT_DIR / 'missing_pdbs.csv'}")

    if not manifest:
        raise RuntimeError("No PDBs copied.")

    df_manifest = pd.DataFrame(manifest)

    df_manifest.to_csv(OUT_DIR / "manifest.csv", index=False)

    with open(OUT_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print("\nDone.")
    print(f"  Copied PDBs: {len(df_manifest)}")
    print(f"  Output dir:  {OUT_DIR}")
    print(f"  CSV:         {OUT_DIR / 'manifest.csv'}")
    print(f"  JSON:        {OUT_DIR / 'manifest.json'}")

    print("\nPreview:")
    print(
        df_manifest[
            [
                "rank",
                "condition_id",
                "seq_id",
                "length",
                "hotspot_config",
                "noise",
                "mean_plddt",
                "rmsd",
                "pdb_file",
            ]
        ].head(15).to_string(index=False)
    )


if __name__ == "__main__":
    main()
