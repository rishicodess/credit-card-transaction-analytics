# Credit Card Transaction Analytics
### End-to-End BFSI Data Analytics Pipeline — Python · SQL · Power BI

**Author:** Rishabh Gupta — Business Analyst | BFSI & Healthcare Domain | Bengaluru
**Contact:** rishabhwork27@gmail.com | [LinkedIn](https://linkedin.com/in/rishabhgupta)

---

## Business Problem

Credit card portfolio managers and product analysts spend significant time
manually aggregating data across systems to answer questions like:

- Which merchant categories drive the most revenue?
- How are high-value customers behaving differently from standard cardholders?
- Where are transaction declines concentrated — and what is the revenue impact?
- How is online vs offline channel share evolving quarter on quarter?
- Which cities and card tiers carry disproportionate risk exposure?

This project simulates an **enterprise-grade analytics workflow** to answer
these questions using a structured end-to-end data pipeline — from raw data
generation to executive-ready dashboards and business insights.

---

## Pipeline Architecture

```
Data Generation (Python + NumPy + Pandas)
         ↓
  Raw CSV — 15,000 transactions | 1,000 customers
         ↓
Data Cleaning & EDA (Pandas + Matplotlib + Seaborn)
  → Null handling, type fixes, outlier flagging
  → 6 EDA charts saved as PNG
         ↓
  Cleaned Dataset — 22 columns
         ↓
SQL Analytics Layer (SQLite)
  → 15 original business queries
  → Window functions, CTEs, YoY/QoQ analysis
         ↓
  Query Results exported to Excel (15 tabs)
         ↓
Power BI Dashboard — 3 pages
  → Executive Overview
  → Customer Analytics
  → Risk & Operations Monitoring
         ↓
Business Report + Data Dictionary
```

---

## Tech Stack

| Layer                | Tool                              |
|----------------------|-----------------------------------|
| Data Generation      | Python, NumPy, Pandas             |
| Data Cleaning & EDA  | Pandas, Matplotlib, Seaborn       |
| Database             | SQLite (portable, zero setup)     |
| SQL Analytics        | 15 original business queries      |
| Visualisation        | Power BI Desktop + Matplotlib     |
| Reporting            | Markdown + Excel                  |

---

## Dataset Overview

| Attribute            | Detail                                        |
|----------------------|-----------------------------------------------|
| Total Transactions   | 15,000                                        |
| Total Customers      | 999 Active                                    |
| Total Revenue        | ₹73.72M (Gross)                               |
| Avg Transaction Value| ₹4,910                                        |
| Approved Transactions| 14,000 (92.55% approval rate)                 |
| Date Range           | Jan 2023 – Dec 2024                           |
| Card Tiers           | Classic · Gold · Platinum · Infinite          |
| Merchant Categories  | Grocery · Dining · Travel · Electronics · +4  |
| Cities               | 10 Indian cities                              |
| Payment Modes        | Online · Swipe · Contactless · EMI            |

---

## Power BI Dashboard — 3 Pages

### Page 1 — Executive Overview

![Executive Overview](Screenshots/executive_overview.png)

**KPI Cards:**
- 15K Total Transactions
- ₹73.72M Total Revenue
- ₹4.91K Avg Transaction Value
- 999 Active Customers
- 14K Approved Transactions

**Visuals:**
- Monthly Revenue Trend (Jan–Dec, both years)
- Revenue by Payment Mode — donut chart
  - Online: ₹29.77M (40.38%) — highest channel
  - Swipe: ₹22.14M (30.03%)
  - Contactless: ₹14.84M (20.12%)
  - EMI: ₹6.97M (9.46%)
- Revenue by Card Tier — horizontal bar
  - Classic leads at ~₹33M total revenue
  - Infinite lowest in volume but highest avg ticket

**Interactive Filters:** City | Payment Mode | Card Tier

---

### Page 2 — Customer Analytics

![Customer Analytics](Screenshots/customer_analytics.png)

**KPI Cards:**
- 999 Active Customers
- ₹4.91K Avg Spend Value
- 4K Weekend Transactions
- ₹249.17K Avg Credit Limit

**Visuals:**
- Revenue by City — horizontal bar chart (Jaipur leads at ~₹7.5M)
- Weekend vs Weekday Spending — comparative bar
  - Weekday: ~₹50M (significantly higher volume)
  - Weekend: ~₹24M
- Customer Distribution by Card Tier — donut chart
  - Classic: 45.67% (6.85K transactions)
  - Gold: 30.57% (4.59K)
  - Platinum: 19.44% (2.92K)
  - Infinite: 4.32% (smallest segment)
- Payment Behavior Analysis — channel breakdown by spend

---

### Page 3 — Risk & Operations Monitoring

![Risk & Operations Monitoring](Screenshots/risk_operations_monitoring.png)

**KPI Cards:**
- 14K Approved Transactions
- 15K Total Processed Transactions
- 2K Outlier Transactions (flagged)
- ₹4.87K Avg Net Transaction

**Visuals:**
- Monthly Approved Transactions Trend — consistent 1,100–1,200 range
- Monthly Outlier Transaction Analysis — ~150–200 flagged per month
- Transaction Status Distribution — donut chart
  - Approved: 92.55% (13.88K)
  - Declined: 4.79% (0.72K)
  - Reversed: 2.66%
- Transaction Volume by Payment Mode — Online leads at ~6K
- Avg Transaction Value by Card Tier — Infinite highest at ~₹5.1K

---

## SQL Business Questions Answered (15 Queries)

| #  | Business Question                                      | SQL Technique              |
|----|--------------------------------------------------------|----------------------------|
| 1  | Top merchant categories by total spend                 | GROUP BY + ORDER BY        |
| 2  | Month-over-month YoY growth (2023 vs 2024)             | CASE WHEN + conditional agg|
| 3  | Top 5 cities per card tier by avg spend                | CTE + ROW_NUMBER window    |
| 4  | Approval rate by payment mode                          | Aggregation + ratio        |
| 5  | High-value transaction share by card tier              | CASE WHEN threshold        |
| 6  | Cumulative monthly spend (2024)                        | SUM OVER window function   |
| 7  | Weekend vs weekday spending behaviour                  | CASE WHEN + GROUP BY       |
| 8  | Top 10 customers by lifetime spend (CLV proxy)         | GROUP BY + ORDER BY        |
| 9  | Cashback yield efficiency by merchant category         | Ratio analysis             |
| 10 | Quarter-on-quarter growth                              | LAG window function        |
| 11 | Cities with highest transaction decline rates          | CASE WHEN + ratio          |
| 12 | Online vs offline channel split by card tier           | Pivot via CASE WHEN        |
| 13 | High-frequency anomaly detection (fraud proxy)         | CTE + frequency threshold  |
| 14 | EMI adoption rate by card tier                         | CASE WHEN + GROUP BY       |
| 15 | Customer composite scorecard — top 20                  | CTE + RANK window function |

---

## Key Business Insights

1. **Online payments dominate at 40.38%** of total revenue — highest channel
   contribution, followed by Swipe at 30.03%

2. **Classic tier drives the most total revenue** due to its 45.67% volume
   share — but Infinite tier customers carry the highest average ticket size
   (₹5.1K vs ₹4.9K overall)

3. **Jaipur leads all cities in total revenue** (~₹7.5M) — a Tier-2 city
   outperforming metros, indicating a concentrated high-value cardholder base

4. **Weekday transactions are 2x weekend volume** — weekend spend at ~₹24M
   vs weekday at ~₹50M, suggesting untapped opportunity for weekend reward multipliers

5. **Transaction approval rate holds at 92.55%** — 4.79% decline rate warrants
   investigation at specific city and payment mode intersections

6. **2,000 outlier transactions flagged** (~13.3% of total) — predominantly in
   Travel and Electronics; valid high-value spends retained for business analysis

---

## Business Analyst Deliverables

Unlike standard data projects, this repository includes BA-grade documentation
alongside the code:

| Deliverable             | Description                                      |
|-------------------------|--------------------------------------------------|
| `project_report.md`     | Executive findings, implications, recommendations|
| `data_dictionary.md`    | Column-level definitions for all 22 fields       |
| `business_queries.sql`  | 15 queries with business context comments        |
| `sql_query_results.xlsx`| All 15 query outputs, one tab per query          |
| EDA Charts (6×PNG)      | Visualisations framed as business insights       |
| Power BI Dashboard      | 3-page interactive PBIX file                     |

---

## Repository Structure

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
├── Dashboard/
│   └── BFSI_Transaction_Analytics_Dashboard.pbix
│
├── Screenshots/
│   ├── executive_overview.png
│   ├── customer_analytics.png
│   └── risk_operations_monitoring.png
│
├── 05_business_docs/
│   ├── project_report.md            # Business insights report
│   ├── sql_query_results.xlsx       # All 15 query outputs
│   └── data_dictionary.md           # Column definitions
│
├── data/
│   ├── raw/transactions.csv
│   └── processed/transactions_clean.csv
│
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/rishicodess/credit-card-transaction-analytics
cd credit-card-transaction-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate dataset
python 01_data_extraction/generate_dataset.py

# 4. Run cleaning pipeline + EDA charts
python 02_data_cleaning/cleaning_pipeline.py

# 5. Run all 15 SQL queries → exports to Excel
python 03_sql_analysis/run_sql_analysis.py

# 6. Open Power BI dashboard
# Open Dashboard/BFSI_Transaction_Analytics_Dashboard.pbix in Power BI Desktop
# Reconnect data source to: data/processed/transactions_clean.csv
```

---

## Future Enhancements

- Real-time streaming dashboard via Power BI + Azure Event Hub
- Fraud detection ML model (Isolation Forest / XGBoost)
- Customer churn prediction pipeline
- Interactive drill-through reporting by customer ID
- API-based live transaction ingestion

---

## Business Use Case

This dashboard is designed for:

| Team                    | Use                                              |
|-------------------------|--------------------------------------------------|
| Banking Operations      | Monitor approval rates and transaction health    |
| Business Analysts       | KPI reporting and trend analysis                 |
| Fraud / Risk Teams      | Outlier flagging and decline pattern monitoring  |
| Product & Strategy      | Channel optimisation and tier performance        |
| Executive Leadership    | Monthly revenue and portfolio overview           |

---

*Built independently as a portfolio project to demonstrate end-to-end
data analytics capability in the BFSI domain.*

*Rishabh Gupta | rishabhwork27@gmail.com | Bengaluru, India*
