# CrockerLabMolecularTBI

Pipeline for aligning Drosophila brain image stacks to a template and measuring fluorescence intensity in predefined ROIs.

---

## Overview

This notebook workflow replaces a manual Fiji process for analyzing many brains consistently.

The pipeline:

* Loads TIFF z-stacks for a brain
* Builds max-intensity projections for each channel
* Aligns the brain to a template using rigid (PCA / center-of-mass) alignment
* Applies predefined ROI masks
* Measures fluorescence intensity within each ROI
* Computes green/red intensity ratios

Main analysis notebook:

```
brain_roi_measure_current.ipynb
```

---

## Repository Structure

```
CrockerLabMolecularTBI/
│
├── roi_masks/
│   ├── AL_left.npy
│   ├── AL_right.npy
│   ├── CX.npy
│   ├── MB_left.npy
│   ├── MB_right.npy
│   ├── PI.npy
│   ├── SEG.npy
│   └── registration_core.npy
│
├── template_data/
│   └── template_reg_img.npy
│
├── brain_roi_measure_current.ipynb
├── brain_roi_measure.ipynb
├── app.py
├── requirements.txt
└── README.md
```

---

## Local Data Structure

Raw microscopy data are expected locally and are **not stored in the repository**.

```
data/
├── template_brain/
│   └── template_image.tif
│
└── brains/
    ├── brain_001/
    │   ├── *_C002Z001.tif
    │   ├── *_C002Z002.tif
    │   ├── ...
    │   ├── *_C003Z001.tif
    │   └── ...
    └── brain_002/
```

---

## Running the Pipeline

1. Open the notebook:

```
brain_roi_measure_current.ipynb
```

2. Set the brain directory:

```python
TEST_BRAIN_DIR = Path("data/brains/<brain_folder>")
```

3. Run the analysis cells in order to:

* load stacks
* compute projections
* align to template
* measure ROI intensities

---

## Channels

The notebook currently assumes:

```
C002 = green
C003 = red
```

Channel assignments may vary between acquisitions. Some datasets may contain empty channels.

---

## ROI Masks

ROI masks are stored as `.npy` files in:

```
roi_masks/
```

`registration_core.npy` is used only for alignment and is not included in final measurements.

---

## Output

For each ROI the notebook computes:

* `green_max`
* `red_max`
* `green_red_ratio`

Example output:

| roi | green_max | red_max | green_red_ratio |
|-----|-----------|---------|-----------------|

---

## Installation

Install dependencies with:

```
pip install -r requirements.txt
```

---

## Notes

* Raw TIFF data are large and should remain local
* ROI masks and template files should remain version controlled
* Alignment is currently rigid (no deformable registration)
