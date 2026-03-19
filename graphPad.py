# Batch ROI Processing Wrapper (Local Google Drive → Papermill → Prism CSV)

import os
import papermill as pm
import pandas as pd

# Local Google Drive folder path
brains_dir = '/Users/gabrielacmclemente/Library/CloudStorage/GoogleDrive-gclemente@middlebury.edu/My Drive/Molecular TBI - Crocker Lab/brain_folder'
results_dir = "results"

os.makedirs(results_dir, exist_ok=True)

print("Scanning for brain folders...\n")

# Find all folders containing .tif files
all_brain_paths = []
for root, dirs, files in os.walk(brains_dir):
    if any(f.endswith(".tif") for f in files):
        all_brain_paths.append(root)

print(f"Found {len(all_brain_paths)} brain folders.\n")


def parse_brain_name(name):
    parts = name.lower().split("_")
    return {
        "Reporter": next((p for p in parts if "mito" in p), "unknown"),
        "Driver": next((p for p in parts if p in ["repo", "nsyb"]), "unknown"),
        "Marker": next((p for p in parts if p in ["draper", "stat"]), "unknown"),
        "Condition": next((p for p in parts if p in ["control", "mild", "moderate", "severe"]), "unknown"),
        "InjuryType": next((p for p in parts if p in ["single", "double"]), "unknown")
    }


all_tables = []

for i, brain_path in enumerate(all_brain_paths, 1):

    brain_name = os.path.basename(brain_path)
    print(f"[{i}/{len(all_brain_paths)}] Processing: {brain_name}")

    output_notebook = os.path.join(results_dir, f"{brain_name}_roi.ipynb")
    output_csv = os.path.join(results_dir, f"{brain_name}_roi.csv")

    try:
        pm.execute_notebook(
            "brain_roi_measure_current.ipynb",
            output_notebook,
            parameters=dict(
                brain_folder=brain_path,
                output_csv=output_csv
            )
        )

        if os.path.exists(output_csv):
            df = pd.read_csv(output_csv)

            df = df.rename(columns={
                "roi": "ROI",
                "green_max": "Green",
                "red_max": "Red",
                "green_red_ratio": "Green_Red_Ratio"
            })

            meta = parse_brain_name(brain_name)
            for key, value in meta.items():
                df[key] = value

            df["Brain"] = brain_name

            desired_cols = [
                "Brain", "ROI", "Green", "Red", "Green_Red_Ratio",
                "Reporter", "Driver", "Marker", "Condition", "InjuryType"
            ]

            df = df[[c for c in desired_cols if c in df.columns]]

            all_tables.append(df)

        else:
            print(f"⚠️ No CSV output for {brain_name}")

    except Exception as e:
        print(f"❌ Error processing {brain_name}: {e}")



if all_tables:

    combined = pd.concat(all_tables, ignore_index=True)

    # Save long-format table (BEST for Prism stats & grouping)
    long_output = os.path.join(results_dir, "prism_long_format.csv")
    combined.to_csv(long_output, index=False)

    print(f"\n✅ Long-format Prism table saved to:\n{long_output}")

    try:
        pivot = combined.pivot_table(
            index="Brain",
            columns="ROI",
            values="Green_Red_Ratio"
        )

        pivot_output = os.path.join(results_dir, "prism_pivot.csv")
        pivot.to_csv(pivot_output)

        print(f"✅ Pivot (wide) table saved to:\n{pivot_output}")

    except Exception as e:
        print(f"⚠️ Could not create pivot table: {e}")

else:
    print("\n⚠️ No data was processed.")