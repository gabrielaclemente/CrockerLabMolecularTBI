# CrockerLabMolecularTBI
Data analysis &amp; output display for the molecular TBI project


for now Im just gonna place whatever I had coded up previously in here, it is a very simple code though!

import pandas as pd
import glob
import os

#look 4 CSV files
files = glob.glob("data/*.csv")
print("Found files:", files)

data = []

#extract mean
for f in files:
    fname = f.lower()
    if "green" in fname:
        channel = "green"
    elif "red" in fname:
        channel = "red"
    else:
        continue
    
    df_csv = pd.read_csv(f)
    mean_int = df_csv["Mean"].iloc[0]  # first row of Mean column
    brain_id = f.split("/")[-1].split("_")[0]

    data.append({
        "brain": brain_id,
        "channel": channel,
        "mean_intensity": mean_int
    })

#data is collected
df_all = pd.DataFrame(data)

#Pivot so we have one row per brain, columns = channels
pivot = df_all.pivot(index="brain", columns="channel", values="mean_intensity")

#Compute Red / Green ratio
pivot["R_G_ratio"] = pivot["red"] / pivot["green"]

output_file = "red_green_ratios.csv"

if os.path.exists(output_file):
    existing = pd.read_csv(output_file, index_col="brain")
    #Append new brains (no duplicates)
    pivot = pd.concat([existing, pivot])
    pivot = pivot[~pivot.index.duplicated(keep="last")]

#updated CSV
pivot.to_csv(output_file)
print("\nSaved/updated file:", output_file)