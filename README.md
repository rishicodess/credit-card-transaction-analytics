# Credit Card Transaction Analytics
### End-to-End BFSI Data Analytics Pipeline

**Author:** Rishabh Gupta — Business Analyst | BFSI & Healthcare Domain | Bengaluru
**Contact:** rishabhwork27@gmail.com | [LinkedIn](https://linkedin.com/in/rishabhgupta)

---

## Business Problem

Credit card portfolio managers and product analysts spend significant time
manually aggregating data across systems to answer questions like:
- Which merchant categories drive the most revenue?
- How are high-value customers behaving differently from standard card holders?
- Where are transaction declines concentrated, and what is the revenue impact?
- How is online vs offline channel share evolving quarter on quarter?

This project simulates an **enterprise-grade analytics workflow** to answer
these questions using a structured data pipeline — from raw data to business insights.

---

## Pipeline Architecture

```
Data Generation (Python + NumPy)
         ↓
  Raw CSV (15,000 transactions)
         ↓
Data Cleaning & EDA (Pandas + Matplotlib)
         ↓
  Cleaned Dataset (22 columns)
         ↓
SQL Analytics Layer (SQLite — 15 business queries)
         ↓
  Query Results (Excel — 15 tabs)
         ↓
Business Report + Visualisations
```

---

## Tech Stack

| Layer              | Tool                        |
|--------------------|-----------------------------|
| Data Generation    | Python, NumPy, Pandas       |
| Data Cleaning      | Pandas, Matplotlib, Seaborn |
| Database           | SQLite (portable, no setup) |
| SQL Analytics      | 15 original business queries|
| Visualisation      | Matplotlib + Power BI       |
| Reporting          | Markdown + Excel            |

---

## Dataset Overview

| Attribute          | Detail                                      |
|--------------------|---------------------------------------------|
| Transactions       | 15,000                                      |
| Customers          | 1,000                                       |
| Date Range         | Jan 2023 – Dec 2024                         |
| Card Tiers         | Classic, Gold, Platinum, Infinite           |
| Merchant Categories| Grocery, Dining, Travel, Electronics, +4   |
| Cities             | 10 Indian cities                            |
| Key Metrics        | Gross amount, cashback, net transaction     |

---

## SQL Business Questions Answered

| #  | Question                                          | Technique Used              |
|----|---------------------------------------------------|-----------------------------|
| 1  | Top merchant categories by total spend            | GROUP BY, ORDER BY          |
| 2  | Month-over-month YoY growth (2023 vs 2024)        | CASE WHEN, conditional agg  |
| 3  | Top 5 cities per card tier by avg spend           | CTE + ROW_NUMBER window     |
| 4  | Approval rate by payment mode                     | Aggregation + ratio         |
| 5  | High-value transaction share by card tier         | CASE WHEN threshold         |
| 6  | Cumulative monthly spend (2024)                   | SUM OVER window function    |
| 7  | Weekend vs weekday spending behaviour             | CASE WHEN + GROUP BY        |
| 8  | Top 10 customers by lifetime spend (CLV proxy)    | GROUP BY + ORDER BY         |
| 9  | Cashback yield efficiency by merchant category    | Ratio analysis              |
| 10 | Quarter-on-quarter growth                         | LAG window function         |
| 11 | Cities with highest transaction decline rates     | CASE WHEN + ratio           |
| 12 | Online vs offline channel split by card tier      | Pivot via CASE WHEN         |
| 13 | High-frequency anomaly detection (fraud proxy)    | CTE + frequency threshold   |
| 14 | EMI adoption rate by card tier                    | CASE WHEN + GROUP BY        |
| 15 | Customer composite scorecard — top 20             | CTE + RANK window function  |

---

## Key Business Insights

1. **Electronics leads spend** despite 8% transaction share — high ticket size
   drives disproportionate revenue contribution
2. **Online payments dominate** at 40.4% channel share, with Swipe showing
   marginally higher decline rates
3. **Jaipur records highest average transaction value** — Tier-2 city premium
   segment opportunity
4. **Weekend transactions** carry higher avg ticket size — opportunity for
   targeted reward multipliers
5. **Infinite card holders** show 2x spending patterns vs Classic tier —
   retention ROI heavily skewed to premium segment

---

## Project Structure

```
credit-card-transaction-analytics/
│
├── 01_data_extraction/
│   └── generate_dataset.py          # Synthetic BFSI dataset generation
│
├── 02_data_cleaning/
│   └── cleaning_pipeline.py         # Cleaning, EDA, 6 visualisation charts
│
├── 03_sql_analysis/
│   ├── business_queries.sql         # 15 annotated SQL queries
│   └── run_sql_analysis.py          # Executes queries → Excel export
│
├── 04_dashboard/
│   └── eda_charts/                  # 6 EDA charts (PNG)
│
├── 05_business_docs/
│   ├── project_report.md            # Business insights report
│   ├── sql_query_results.xlsx       # All 15 query outputs
│   └── data_dictionary.md           # Column definitions
│
├── data/
│   ├── raw/transactions.csv         # Generated raw data
│   └── processed/transactions_clean.csv
│
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/rishabhgupta/credit-card-transaction-analytics
cd credit-card-transaction-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate dataset
python 01_data_extraction/generate_dataset.py

# 4. Run cleaning pipeline + EDA charts
python 02_data_cleaning/cleaning_pipeline.py

# 5. Run all 15 SQL queries
python 03_sql_analysis/run_sql_analysis.py

# Results saved to 05_business_docs/sql_query_results.xlsx
```

---

## BA Deliverables in This Project

Unlike standard data projects, this repository includes business analyst
deliverables alongside the code:

- **Business Report** — findings, implications, and recommendations
- **Data Dictionary** — column-level definitions for every field
- **Annotated SQL** — every query includes business context comments
- **EDA Charts** — visualisations framed as business insights, not just plots

---

*Built independently as a portfolio project to demonstrate end-to-end
data analytics capability in the BFSI domain.*
