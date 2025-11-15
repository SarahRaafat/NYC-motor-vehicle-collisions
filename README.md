# NYC Motor Vehicle Collisions – Data Visualization Project

## 1. Overview

This project analyzes NYC Motor Vehicle Collisions (2012–2025) using:
- **Crashes dataset**
- **Persons dataset**
from NYC Open Data, integrated via `COLLISION_ID`.

We clean, integrate, and explore the data, then prepare a merged dataset for an interactive Dash dashboard.

## 2. Data Sources

- NYC Motor Vehicle Collisions – Crashes  
  https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

- NYC Motor Vehicle Collisions – Persons  
  https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu

## 3. Project Steps

1. **EDA**
   - Crash distribution by year / month / hour.
   - Borough distribution.
   - Injuries & fatalities summary.
   - Coordinate coverage & duplicates.

2. **Cleaning**
   - Normalize IDs, ZIP, borough names.
   - Handle missing values (drop required keys, impute non-critical columns).
   - Domain-based outlier handling (NYC bounding box, year range, non-negative counts).

3. **Integration**
   - Aggregate Persons per `COLLISION_ID` (counts, injuries, fatalities, optional age/type).
   - LEFT merge Crashes × Persons → one row per crash.

4. **Post-Integration Analysis**
   - Coverage statistics.
   - Null rates for key variables.
   - Plots: crashes by borough, persons per crash, injured vs hour of day.

5. **Dashboard Data**
   - Export `integrated_collisions.csv` and `data/dashboard_ready.csv` for the Dash app.

## 4. How to Run

6. **Research Questions**
- Which borough has the more frequent accidents (crashes)?
- Which year has the highest casualties? (highest no. of people who died due to crashes) 

```bash
pip install -r requirements.txt
jupyter notebook
# open the main notebook and run all cells
