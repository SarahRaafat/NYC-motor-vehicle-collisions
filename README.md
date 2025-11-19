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

## **4. Installation & Setup**

### **1. Clone the project**

```bash
git clone <your-repo-link>
cd nyc-collisions
```

### **2. Create a virtual environment (recommended)**

```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## **5. How to Run the Jupyter Notebook**

```bash
jupyter notebook
```

Then open:
**`NYC_Collisions_Analysis.ipynb`**
Run all cells in order.

---

## **6. How to Run the Dash Dashboard**

Move into the dashboard directory (if applicable):

```bash
cd dashboard
python app.py
```

The dashboard will start at:
👉 [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

---

## **7. Deployment Instructions (Local / Production)**

### **A) Local Deployment**

1. Ensure the virtual environment is activated
2. Ensure all datasets are in `data/`
3. Run:

```bash
python app.py
```

### **B) Production Deployment (Optional if required by prof)**

You can deploy on:

* **Render**
* **Railway**
* **Heroku (if available)**
* **Dash Enterprise**
  Include:
* `requirements.txt`
* `Procfile` (for Heroku)
* Your `app.py`
* Static files

---

## **8. Team Members & Contributions**

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
* Dropdowns, filters
* Year, Borough, Hour graphs

---

## **9. Research Questions Answered**

Gamila
* Which borough has the more frequent accidents (crashes)?
* Which year has the highest casualties? (highest no. of people who died due to crashes) 
Sarah
* What age group is most vulnerable to severe crashes?
* Does crash severity vary by time of day? (Peak severity hours) 
Omar
*Is there a relationship between person’s age and injury?
*Which gender gets into more frequent crashes?
Reem
*
*
Mostafa
*
*
---

## **10. Output Files**

Inside `/data`:

* `clean_crashes.csv`
* `clean_persons.csv`
* `clean_persons_agg.csv`
* `integrated_collisions.csv`
* `dashboard_ready.csv`