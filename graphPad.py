# Batch ROI Processing Wrapper (Local Google Drive → Papermill → Prism CSV)

import os
import papermill as pm
import pandas as pd

# Local Google Drive folder path
brains_dir = '/Users/gabrielacmclemente/Library/CloudStorage/GoogleDrive-gclemente@middlebury.edu/My Drive/Molecular TBI - Crocker Lab/brain_folder'
results_dir = "results"

# Make results directory if it doesn't exist
os.makedirs(results_dir, exist_ok=True)

print("Scanning for brain folders...\n")

# Find all folders containing .tif files
all_brain_paths = []
for root, dirs, files in os.walk(brains_dir):
    if any(f.endswith(".tif") for f in files):
        all_brain_paths.append(root)

print(f"Found {len(all_brain_paths)} brain folders.\n")

# Function to parse metadata from folder name
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

# Process each brain folder using Papermill
for brain_path in all_brain_paths:
    brain_name = os.path.basename(brain_path)
    print(f"Processing: {brain_name}")

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

            # Add metadata columns
            meta = parse_brain_name(brain_name)
            for key, value in meta.items():
                df[key] = value

            df["Brain"] = brain_name
            all_tables.append(df)

        else:
            print(f"⚠️ No CSV output for {brain_name}")

    except Exception as e:
        print(f"❌ Error processing {brain_name}: {e}")

# Combine all CSVs into one Prism-ready table
if all_tables:
    combined = pd.concat(all_tables, ignore_index=True)
    output_file = os.path.join(results_dir, "prism_table.csv")
    combined.to_csv(output_file, index=False)
    print(f"\n✅ Finished! Combined Prism table saved to:\n{output_file}")
else:
    print("\n⚠️ No data was processed.")