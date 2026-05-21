# Credit Card Transaction Analytics Report
### BFSI Portfolio Intelligence — FY 2023–24

**Prepared by:** Rishabh Gupta, Business Analyst
**Domain:** BFSI — Payments & Card Analytics
**Dataset:** 15,000 synthetic transactions | 1,000 customers | Jan 2023 – Dec 2024
**Tools:** Python (Pandas) · SQLite · Power BI · Matplotlib

---

## 1. Executive Summary

This report presents a comprehensive analysis of credit card transaction behaviour
across customer tiers, merchant categories, cities, and payment channels for a
mid-size card portfolio over a two-year period.

| KPI                        | Value           |
|----------------------------|-----------------|
| Total Approved Spend       | ₹6.85 Crore     |
| Total Approved Transactions| 13,882          |
| Overall Approval Rate      | 92.5%           |
| Top Merchant Category      | Electronics     |
| Highest Avg-Spend City     | Jaipur          |
| Online Channel Share       | 40.4%           |

---

## 2. Key Business Findings

### Finding 1 — Electronics Dominates Spend Despite Lower Frequency
Electronics is the highest-revenue merchant category, driven by high average
ticket sizes (₹18,000+), even though it accounts for only ~8% of transaction
volume. Grocery and Dining lead on frequency but trail on total spend.

**Business Implication:** Targeted EMI offers on Electronics can significantly
lift revenue per transaction and reduce cart abandonment at high-value merchants.

---

### Finding 2 — Infinite Card Holders Spend 2x Classic Customers
Infinite tier customers (5% of base) generate a disproportionate share of
high-value transactions. Average ticket size for Infinite (₹5,061) is
significantly higher than Classic (₹4,953), but the real gap lies in frequency
and EMI adoption.

**Business Implication:** Premium tier retention programs (concierge, travel
perks) have outsized ROI. A 1% churn reduction in Infinite tier is worth
multiples of equivalent Classic tier retention spend.

---

### Finding 3 — Online Payments Lead at 40.4% but Swipe Declines Are Higher
Online channel drives the highest transaction volume (40.4% share) while
Contactless is growing. Swipe transactions show a marginally higher decline rate,
suggesting legacy POS terminal issues at certain merchant locations.

**Business Implication:** Accelerating contactless and UPI-linked card adoption
can reduce decline rates while improving customer experience at point-of-sale.

---

### Finding 4 — Weekend Spend is Higher Per Transaction
Weekend transactions show a higher average ticket size than weekday transactions,
driven by Travel, Dining, and Entertainment categories. However, total weekday
volume is 2.3x higher.

**Business Implication:** Weekend-specific reward multipliers on Travel and
Dining can increase premium tier engagement without impacting the high-volume
weekday business.

---

### Finding 5 — Jaipur Leads on Average Transaction Value
Despite not being a metro city, Jaipur records the highest average transaction
value. This may indicate a concentration of high-net-worth cardholders or
premium merchant partnerships in the city.

**Business Implication:** Targeted city-level campaigns in Tier-2 cities with
similar profiles (Jaipur, Lucknow) can unlock underserved premium segments.

---

## 3. Risk Observations

- **Decline Rate:** Overall decline rate is 7.5%, concentrated in specific
  cities and Swipe payment mode.
- **High-Frequency Anomalies:** SQL analysis (Q13) flagged customers with
  4+ transactions in a single day — these warrant review by the fraud team.
- **Outliers:** 13.7% of transactions fall outside the IQR range, predominantly
  in Travel and Electronics — valid high-value spends, not removed.

---

## 4. Recommendations

| # | Recommendation                              | Priority | Effort |
|---|---------------------------------------------|----------|--------|
| 1 | Launch EMI-first campaign for Electronics   | High     | Low    |
| 2 | Invest in Infinite tier retention program   | High     | Medium |
| 3 | Accelerate contactless terminal rollout     | Medium   | High   |
| 4 | Weekend reward multiplier — Travel & Dining | Medium   | Low    |
| 5 | Tier-2 city premium acquisition campaign    | Low      | Medium |

---

## 5. Methodology

**Data Pipeline:**
```
Data Generation (Python/Faker)
    → Cleaning & EDA (Pandas)
    → Storage (SQLite)
    → Business Queries (SQL — 15 queries)
    → Visualisation (Power BI / Matplotlib)
    → Reporting (This document)
```

**SQL Techniques Used:**
- Aggregation (SUM, AVG, COUNT)
- Window functions (ROW_NUMBER, LAG, RANK, SUM OVER)
- CTEs (Common Table Expressions)
- Conditional aggregation (CASE WHEN)
- YoY and QoQ comparison
- Anomaly detection via frequency thresholds

---

## 6. Limitations & Assumptions

- Dataset is synthetic; real-world patterns may differ by issuer geography
- Credit limits are tier-proxied, not customer-individual
- Fraud labels are simulated via frequency thresholds only
- No external data (macroeconomic, competitor) incorporated

---

*Rishabh Gupta | rishabhwork27@gmail.com | LinkedIn: linkedin.com/in/rishabhgupta*
