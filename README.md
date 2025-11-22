# **NYC Motor Vehicle Collisions – Data Visualization Project**

## **1. Overview**

This project analyzes NYC Motor Vehicle Collisions (2012–2025) using two NYC Open Data datasets:

* **Crashes dataset**
* **Persons dataset**

The workflow includes **data cleaning**, **exploration**, **integration**, and preparing an integrated dataset for an **interactive Dash dashboard** visualizing crash patterns across NYC.

---

## **2. Data Sources**

* Motor Vehicle Collisions – **Crashes**
  [https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)

* Motor Vehicle Collisions – **Persons**
  [https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu)

---

## **3. Project Workflow**

### **A) Exploratory Data Analysis (EDA)**

* Crash distribution by **year**, **month**, **hour**
* Borough distribution
* Injuries and fatalities summary
* Coordinate coverage and duplicates detection

### **B) Data Cleaning**

* Datetime normalization
* ID unification using `COLLISION_ID`
* Borough and ZIP standardization
* Missing-value strategy

  * Drop critical fields (`COLLISION_ID`, datetime)
  * Impute categorical values (“UNKNOWN”)
  * Domain-filter latitude/longitude
* Numeric domain cleaning

  * Remove negatives
  * Correct out-of-range ages
  * Cap unreasonable values

### **C) Data Integration**

* Aggregate Persons dataset per `COLLISION_ID`
* Compute:

  * persons_count
  * injured_count
  * killed_count
  * median_age
  * vehicle involvement
* LEFT join Crashes × Persons
* Produce a **single crash-level dataset**

### **D) Post-Integration Validation**

* Check null rates
* Compare injury totals pre/post merge
* Verify coordinates consistency
* Visual checks:

  * persons per crash
  * injured by hour
  * borough crash distribution

### **E) Dashboard Preparation**

* Export:

  * `clean_crashes.csv`
  * `clean_persons.csv`
  * `clean_persons_agg.csv`
  * `integrated_collisions.csv`
  * `dashboard_ready.csv`

---

## **4. Deployment Instructions:

* **Render** (I used render to deploy)
1. I created the requirements.txt file as well as the procfile and app.py.
2. Then I updated the csv path because Render is a little different when writing the path.
3. I also added the dashboard_ready.csv to the git repository so it can be seen.
4. I commited and pushed into github.
5. The repository was made public.
6. On Render I chose "web service" and pasted the repository link in the "insert link for repository" area.
7. After it built the app and deployed I copied the link and tested on it.

## **5. Deployment Links: **
- For sample data: https://nyc-motor-vehicle-collisions.onrender.com/ (20k)
Search works for sample: BROOKLYN Sedan Passing or Lane Usage Improper
Search thar works for sample: MANHATTAN Station Wagon/Sport Utility Vehicle Following Too Closely

- For full data: https://nyc-motor-vehicle-collisions-2.onrender.com/ 
Searh1: BRONX Sedan Driver Inexperience
Search2: QUEENS Bike Unsafe Speed
Search3: BROOKLYN Sedan Passing or Lane Usage Improper
Filter1: 2021, BRONX, Sedan, Driver Inexperince, Tuesday
Filter2: 2021, MANHATTAN, Station Wagon/Sport Utility Vehicle, Following Too Closely, Saturday
Filter3: 2022, QUEENS, Sedan, Unsafe Speed, Saturday

---

## **6. Team Members & Contributions**

**Team of 5 Members**

### **Member 1 – Sarah**

* EDA planning & execution
* Cleaning documentation and architectural structure
* Missing-value strategy
* Integration (User authentication tasks)
* Crash map visualization
* Export final dashboard-ready dataset
* Final polishing

### **Member 2 – Mostafa**

* Initial dataset exploration
* Datetime cleaning functions
* Borough unification + ZIP cleaning
* Handling numeric outliers

### **Member 3 – Reem**

* Persons dataset cleaning
* Age corrections
* Injury/fatality aggregation
* Pre-integration checks

### **Member 4 – Omar**

* Merge logic (LEFT join)
* Integrity checks (counts, mismatches)
* Creation of merged indicators/columns

### **Member 5 – Gamila**

* Dashboard layout
* Dropdowns filters, visualizations
* Deployment

---

## **7. Research Questions Answered**

# Research Questions

## Gamila
- Which borough has the more frequent accidents (crashes)?
- Which year has the highest casualties? (highest no. of people who died due to crashes)

## Sarah
- What age group is most vulnerable to severe crashes?
- Does crash severity vary by time of day? (Peak severity hours)

## Omar
- Is there a relationship between person’s age and injury?
- Is there a relationship between the number of persons involved and crash fatality rate?

## Reem
- Which contributing factors have the highest fatality rate (not just counts)?
- Are weekends more dangerous than weekdays? (severity pattern analysis)

## Mostafa
- Which crash hour has the highest rate of fatal collisions per crash?
- How does the fatality risk per collision vary by vehicle type?

---

## **8. Output Files**

Inside `/data`:

* `clean_crashes.csv`
* `clean_persons.csv`
* `clean_persons_agg.csv`
* `integrated_collisions.csv`
* `dashboard_ready.csv`

