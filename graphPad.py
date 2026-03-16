#This will essentially be generating a table output in csv, which we will be able to plug directly into prism graphpad for image analysis

import os
import papermill as pm
import pandas as pd

brains_dir = "brains"
results_dir = "results"

os.makedirs(results_dir, exist_ok=True)

all_tables = []

for brain in os.listdir(brains_dir):

    brain_path = os.path.join(brains_dir, brain)

    if not os.path.isdir(brain_path):
        continue

    print(f"Processing {brain}")

    output_notebook = f"{results_dir}/{brain}_roi_output.ipynb"

    #runs the ROI notebook
    pm.execute_notebook(
        "brain_roi_measure_current.ipynb",
        output_notebook,
        parameters=dict(brain_folder=brain_path)
    )

    #assumes ROI notebook exports a CSV --> we are not there quite yet, I mean there is an output but yeah
    csv_file = os.path.join(brain_path, "roi_results.csv")

    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        df["Brain"] = brain
        all_tables.append(df)

#combines all the brains
if all_tables:
    combined = pd.concat(all_tables, ignore_index=True)
    combined.to_csv(f"{results_dir}/prism_table.csv", index=False)

print("Finished. Prism table saved.")