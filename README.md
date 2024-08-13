# Sudden Cardiac Death Database (SDDB) - Data Extraction

This project utilizes the Sudden Cardiac Death Database (SDDB) provided by PhysioNet to extract and preprocess ECG data for research purposes. The focus is on patients who experienced ventricular fibrillation (VF). We specifically extract 20-second continuous rhythm segments of ECG data at different time intervals before the onset of VF.

## Overview

The SDDB contains Holter recordings from patients who experienced sustained ventricular tachyarrhythmia and, in many cases, actual cardiac arrest. The database includes:
- 18 patients with underlying sinus rhythm
- 1 patient who was continuously paced
- 4 patients with atrial fibrillation

## Data Extraction Process

### Objectives

For each patient who experienced VF, the following ECG data segments are extracted:
- 20-second continuous ECG rhythm segments from 30 to 60 minutes before VF onset.
- 20-second continuous ECG rhythm segments from 60 to 120 minutes before VF onset.
- 20-second continuous ECG rhythm segments from 120 to 180 minutes before VF onset.

### Data Extraction Procedure

1. **Load Data:**
   - The ECG data and annotation files are loaded using the WFDB Python package.

2. **Convert Time:**
   - VF onset times and durations are converted into seconds for precise indexing.

3. **Segment Extraction:**
   - For each patient, extract 20-second continuous ECG rhythm segments at the specified intervals:
     - 30 to 60 minutes before VF onset
     - 60 to 120 minutes before VF onset
     - 120 to 180 minutes before VF onset

4. **Data Saving:**
   - Extracted segments are saved as `.npy` files for further analysis.

## Directory Structure

- `src/`: Source code for data extraction and processing.
- `preprocess/`: Contains scripts for data extraction and preprocessing.
- `models/`: Contains scripts for modeling and evaluation.
- `data/`: Directory containing raw ECG data files.
- `results/`: Directory where processed `.npy` files are saved.

## Example Usage

Run the provided Python scripts to perform data extraction as follows:

```bash
python src/preprocess/generate_ecg_segments_from_vf_onset.py --interval_start 30 --interval_end 60 
python src/preprocess/generate_ecg_segments_from_vf_onset.py --interval_start 60 --interval_end 120 
python src/preprocess/generate_ecg_segments_from_vf_onset.py --interval_start 120 --interval_end 180 
