"""
========================================================
  SQL Analysis Runner
  Author  : Rishabh Gupta
  Domain  : BFSI – Credit Card Transaction Analytics
  Purpose : Load cleaned data into SQLite, execute all
            15 business queries, export results to Excel
========================================================
"""

import pandas as pd
import sqlite3
import os
import warnings
warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────
BASE       = os.path.join(os.path.dirname(__file__), "..")
CLEAN_CSV  = os.path.join(BASE, "data", "processed", "transactions_clean.csv")
DB_PATH    = os.path.join(BASE, "data", "processed", "transactions.db")
EXCEL_OUT  = os.path.join(BASE, "05_business_docs", "sql_query_results.xlsx")

# ── Load CSV → SQLite ─────────────────────────────────
print("\n" + "="*55)
print("  Loading data into SQLite...")
print("="*55)

df = pd.read_csv(CLEAN_CSV)

# Convert categorical column for SQLite
df["txn_size_bucket"] = df["txn_size_bucket"].astype(str)

conn = sqlite3.connect(DB_PATH)
df.to_sql("transactions", conn, if_exists="replace", index=False)
print(f"  ✅ {len(df):,} rows loaded into SQLite → {DB_PATH}")

# ── Define all 15 queries ─────────────────────────────
queries = {

    "Q01_Top_Categories_By_Spend": """
        SELECT
            merchant_category,
            COUNT(*)                          AS total_transactions,
            ROUND(SUM(gross_amount), 2)       AS total_spend,
            ROUND(AVG(gross_amount), 2)       AS avg_transaction_value,
            ROUND(SUM(cashback_amount), 2)    AS total_cashback_paid
        FROM transactions
        WHERE is_approved = 1
        GROUP BY merchant_category
        ORDER BY total_spend DESC
        LIMIT 10
    """,

    "Q02_YoY_Monthly_Growth": """
        SELECT
            transaction_month,
            SUM(CASE WHEN transaction_year=2023 THEN gross_amount ELSE 0 END)
                AS spend_2023,
            SUM(CASE WHEN transaction_year=2024 THEN gross_amount ELSE 0 END)
                AS spend_2024,
            ROUND(
                (SUM(CASE WHEN transaction_year=2024 THEN gross_amount ELSE 0 END)
               - SUM(CASE WHEN transaction_year=2023 THEN gross_amount ELSE 0 END))
              * 100.0
              / NULLIF(SUM(CASE WHEN transaction_year=2023
                               THEN gross_amount ELSE 0 END), 0)
            , 2) AS yoy_growth_pct
        FROM transactions
        WHERE is_approved = 1
        GROUP BY transaction_month
        ORDER BY transaction_month
    """,

    "Q03_Top5_Cities_Per_CardTier": """
        WITH city_tier_avg AS (
            SELECT city, card_tier,
                ROUND(AVG(gross_amount), 2) AS avg_spend,
                COUNT(*)                    AS txn_count
            FROM transactions
            WHERE is_approved = 1
            GROUP BY city, card_tier
        ),
        ranked AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY card_tier ORDER BY avg_spend DESC
                ) AS rank_within_tier
            FROM city_tier_avg
        )
        SELECT city, card_tier, avg_spend, txn_count, rank_within_tier
        FROM ranked
        WHERE rank_within_tier <= 5
        ORDER BY card_tier, rank_within_tier
    """,

    "Q04_Approval_Rate_By_PaymentMode": """
        SELECT
            payment_mode,
            COUNT(*)                                        AS total_attempts,
            SUM(is_approved)                                AS approved,
            ROUND(SUM(is_approved)*100.0/COUNT(*), 2)       AS approval_rate_pct,
            ROUND(SUM(CASE WHEN status='Declined'
                           THEN gross_amount ELSE 0 END),2)  AS declined_value_lost
        FROM transactions
        GROUP BY payment_mode
        ORDER BY approval_rate_pct DESC
    """,

    "Q05_HighValue_Txns_By_CardTier": """
        SELECT
            card_tier,
            COUNT(*)                                                AS total_txns,
            SUM(CASE WHEN gross_amount>15000 THEN 1 ELSE 0 END)    AS high_value_txns,
            ROUND(SUM(CASE WHEN gross_amount>15000 THEN 1 ELSE 0 END)
                  *100.0/COUNT(*), 2)                               AS high_value_pct,
            ROUND(AVG(gross_amount), 2)                             AS avg_txn_value,
            ROUND(SUM(gross_amount), 2)                             AS total_spend
        FROM transactions
        WHERE is_approved = 1
        GROUP BY card_tier
        ORDER BY total_spend DESC
    """,

    "Q06_Cumulative_Monthly_Spend_2024": """
        WITH monthly_spend AS (
            SELECT transaction_month,
                ROUND(SUM(gross_amount), 2) AS monthly_spend
            FROM transactions
            WHERE is_approved=1 AND transaction_year=2024
            GROUP BY transaction_month
        )
        SELECT
            transaction_month,
            monthly_spend,
            ROUND(SUM(monthly_spend) OVER (
                ORDER BY transaction_month
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ), 2) AS cumulative_spend
        FROM monthly_spend
        ORDER BY transaction_month
    """,

    "Q07_Weekend_vs_Weekday": """
        SELECT
            CASE WHEN is_weekend=1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
            COUNT(*)                        AS total_transactions,
            ROUND(SUM(gross_amount), 2)     AS total_spend,
            ROUND(AVG(gross_amount), 2)     AS avg_spend,
            ROUND(SUM(cashback_amount), 2)  AS cashback_issued
        FROM transactions
        WHERE is_approved = 1
        GROUP BY is_weekend
    """,

    "Q08_Top10_Customers_LTV": """
        SELECT
            customer_id, card_tier, city,
            COUNT(*)                        AS total_transactions,
            ROUND(SUM(gross_amount), 2)     AS lifetime_spend,
            ROUND(SUM(cashback_amount), 2)  AS total_cashback_earned,
            ROUND(AVG(gross_amount), 2)     AS avg_txn_value
        FROM transactions
        WHERE is_approved = 1
        GROUP BY customer_id, card_tier, city
        ORDER BY lifetime_spend DESC
        LIMIT 10
    """,

    "Q09_Cashback_Yield_By_Category": """
        SELECT
            merchant_category,
            ROUND(SUM(gross_amount), 2)                       AS total_spend,
            ROUND(SUM(cashback_amount), 2)                    AS total_cashback,
            ROUND(SUM(cashback_amount)*100.0
                  /NULLIF(SUM(gross_amount),0), 3)            AS cashback_yield_pct,
            COUNT(DISTINCT customer_id)                        AS unique_customers
        FROM transactions
        WHERE is_approved = 1
        GROUP BY merchant_category
        ORDER BY cashback_yield_pct DESC
    """,

    "Q10_QoQ_Growth": """
        WITH quarterly AS (
            SELECT transaction_year, transaction_quarter,
                COUNT(*)                    AS txn_count,
                ROUND(SUM(gross_amount),2)  AS total_spend
            FROM transactions
            WHERE is_approved = 1
            GROUP BY transaction_year, transaction_quarter
        )
        SELECT
            transaction_year, transaction_quarter,
            txn_count, total_spend,
            LAG(txn_count) OVER (
                ORDER BY transaction_year, transaction_quarter
            ) AS prev_quarter_count,
            ROUND(
                (txn_count - LAG(txn_count) OVER (
                    ORDER BY transaction_year, transaction_quarter))
                *100.0
                /NULLIF(LAG(txn_count) OVER (
                    ORDER BY transaction_year, transaction_quarter),0)
            ,2) AS qoq_growth_pct
        FROM quarterly
        ORDER BY transaction_year, transaction_quarter
    """,

    "Q11_Decline_Rate_By_City": """
        SELECT
            city,
            COUNT(*)                                               AS total_txns,
            SUM(CASE WHEN status='Declined' THEN 1 ELSE 0 END)    AS declined,
            ROUND(SUM(CASE WHEN status='Declined' THEN 1 ELSE 0 END)
                  *100.0/COUNT(*), 2)                              AS decline_rate_pct,
            ROUND(SUM(CASE WHEN status='Declined'
                           THEN gross_amount ELSE 0 END), 2)       AS declined_value
        FROM transactions
        GROUP BY city
        ORDER BY decline_rate_pct DESC
    """,

    "Q12_Online_vs_Offline_By_Tier": """
        SELECT
            card_tier,
            ROUND(SUM(CASE WHEN payment_mode='Online'
                           THEN gross_amount ELSE 0 END),2)     AS online_spend,
            ROUND(SUM(CASE WHEN payment_mode IN ('Swipe','Contactless')
                           THEN gross_amount ELSE 0 END),2)     AS offline_spend,
            ROUND(SUM(CASE WHEN payment_mode='Emi'
                           THEN gross_amount ELSE 0 END),2)     AS emi_spend,
            ROUND(SUM(gross_amount),2)                          AS total_spend,
            ROUND(SUM(CASE WHEN payment_mode='Online'
                           THEN gross_amount ELSE 0 END)
                  *100.0/NULLIF(SUM(gross_amount),0),2)         AS online_share_pct
        FROM transactions
        WHERE is_approved = 1
        GROUP BY card_tier
        ORDER BY total_spend DESC
    """,

    "Q13_High_Frequency_Anomalies": """
        WITH daily_freq AS (
            SELECT customer_id,
                DATE(transaction_date)  AS txn_day,
                COUNT(*)                AS txns_in_day,
                ROUND(SUM(gross_amount),2) AS day_spend
            FROM transactions
            WHERE is_approved = 1
            GROUP BY customer_id, DATE(transaction_date)
        )
        SELECT customer_id, txn_day, txns_in_day, day_spend
        FROM daily_freq
        WHERE txns_in_day >= 4
        ORDER BY txns_in_day DESC
        LIMIT 20
    """,

    "Q14_EMI_Adoption_By_Tier": """
        SELECT
            card_tier,
            COUNT(*)                                                AS total_txns,
            SUM(CASE WHEN payment_mode='Emi' THEN 1 ELSE 0 END)    AS emi_txns,
            ROUND(SUM(CASE WHEN payment_mode='Emi' THEN 1 ELSE 0 END)
                  *100.0/COUNT(*), 2)                               AS emi_adoption_pct,
            ROUND(AVG(CASE WHEN payment_mode='Emi'
                           THEN gross_amount END), 2)               AS avg_emi_ticket
        FROM transactions
        WHERE is_approved = 1
        GROUP BY card_tier
        ORDER BY emi_adoption_pct DESC
    """,

    "Q15_Customer_Scorecard_Top20": """
        WITH customer_stats AS (
            SELECT customer_id, card_tier, city,
                COUNT(*)                                              AS total_txns,
                ROUND(SUM(gross_amount),2)                            AS total_spend,
                ROUND(AVG(gross_amount),2)                            AS avg_spend,
                SUM(CASE WHEN status='Declined' THEN 1 ELSE 0 END)   AS declines,
                ROUND(SUM(CASE WHEN status='Declined' THEN 1 ELSE 0 END)
                      *100.0/COUNT(*),2)                              AS decline_rate_pct,
                ROUND(SUM(cashback_amount),2)                         AS total_cashback
            FROM transactions
            GROUP BY customer_id, card_tier, city
        ),
        scored AS (
            SELECT *,
                ROUND((total_spend/10000.0)+(total_txns*2.0)
                      -(decline_rate_pct*5.0), 2)   AS customer_score
            FROM customer_stats
        )
        SELECT customer_id, card_tier, city,
               total_txns, total_spend, avg_spend,
               decline_rate_pct, total_cashback,
               customer_score,
               RANK() OVER (ORDER BY customer_score DESC) AS score_rank
        FROM scored
        ORDER BY customer_score DESC
        LIMIT 20
    """,
}

# ── Run All Queries & Save to Excel ───────────────────
print("\n" + "="*55)
print("  Running 15 SQL queries...")
print("="*55)

os.makedirs(os.path.dirname(EXCEL_OUT), exist_ok=True)

with pd.ExcelWriter(EXCEL_OUT, engine="openpyxl") as writer:
    for qname, sql in queries.items():
        result = pd.read_sql_query(sql, conn)
        sheet  = qname[:31]          # Excel tab limit = 31 chars
        result.to_excel(writer, sheet_name=sheet, index=False)
        print(f"  ✓ {qname:<42}  {len(result):>4} rows")

conn.close()

print(f"\n  ✅ All results exported → {EXCEL_OUT}")
print("="*55 + "\n")
