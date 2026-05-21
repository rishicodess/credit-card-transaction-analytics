-- ============================================================
--  Credit Card Transaction Analytics — Business SQL Queries
--  Author  : Rishabh Gupta
--  Domain  : BFSI – Transaction Intelligence
--  DB      : SQLite / MySQL compatible
-- ============================================================
-- HOW TO USE
--   SQLite : Run via DB Browser for SQLite (free tool)
--   MySQL  : Run via MySQL Workbench after loading data
--   Python : Executed automatically by run_sql_analysis.py
-- ============================================================


-- ── TABLE SETUP (run once) ──────────────────────────────────

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id      TEXT,
    customer_id         TEXT,
    transaction_date    TEXT,
    merchant_category   TEXT,
    gross_amount        REAL,
    city                TEXT,
    payment_mode        TEXT,
    status              TEXT,
    card_tier           TEXT,
    cashback_rate       REAL,
    credit_limit        INTEGER,
    cashback_amount     REAL,
    net_transaction     REAL,
    transaction_year    INTEGER,
    transaction_month   INTEGER,
    transaction_quarter INTEGER,
    day_of_week         TEXT,
    utilisation_flag    INTEGER,
    txn_size_bucket     TEXT,
    is_weekend          INTEGER,
    is_approved         INTEGER,
    is_outlier          INTEGER
);


-- ============================================================
-- Q1. What are the top 10 merchant categories by total spend?
--     (Classic product-company SQL — aggregation + sort)
-- ============================================================
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
LIMIT 10;


-- ============================================================
-- Q2. Month-over-Month transaction volume trend (2023 vs 2024)
--     (YoY comparison — Amex / Mastercard interview favourite)
-- ============================================================
SELECT
    transaction_month,
    SUM(CASE WHEN transaction_year = 2023 THEN gross_amount ELSE 0 END)
        AS spend_2023,
    SUM(CASE WHEN transaction_year = 2024 THEN gross_amount ELSE 0 END)
        AS spend_2024,
    ROUND(
        (SUM(CASE WHEN transaction_year = 2024 THEN gross_amount ELSE 0 END)
       - SUM(CASE WHEN transaction_year = 2023 THEN gross_amount ELSE 0 END))
      * 100.0
      / NULLIF(SUM(CASE WHEN transaction_year = 2023 THEN gross_amount ELSE 0 END), 0),
    2) AS yoy_growth_pct
FROM transactions
WHERE is_approved = 1
GROUP BY transaction_month
ORDER BY transaction_month;


-- ============================================================
-- Q3. Top 5 cities by average transaction value per card tier
--     (Window function — ROW_NUMBER partitioned by tier)
-- ============================================================
WITH city_tier_avg AS (
    SELECT
        city,
        card_tier,
        ROUND(AVG(gross_amount), 2) AS avg_spend,
        COUNT(*)                     AS txn_count
    FROM transactions
    WHERE is_approved = 1
    GROUP BY city, card_tier
),
ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY card_tier
            ORDER BY avg_spend DESC
        ) AS rank_within_tier
    FROM city_tier_avg
)
SELECT city, card_tier, avg_spend, txn_count, rank_within_tier
FROM ranked
WHERE rank_within_tier <= 5
ORDER BY card_tier, rank_within_tier;


-- ============================================================
-- Q4. Transaction approval rate by payment mode
--     (Operational KPI — conversion funnel thinking)
-- ============================================================
SELECT
    payment_mode,
    COUNT(*)                                        AS total_attempts,
    SUM(is_approved)                                AS approved,
    ROUND(SUM(is_approved) * 100.0 / COUNT(*), 2)  AS approval_rate_pct,
    ROUND(SUM(CASE WHEN status = 'Declined'
                   THEN gross_amount ELSE 0 END), 2) AS declined_amount_lost
FROM transactions
GROUP BY payment_mode
ORDER BY approval_rate_pct DESC;


-- ============================================================
-- Q5. Which customer segment (card tier) drives the most
--     high-value transactions (>₹15,000)?
--     (Customer segmentation — Amex interview question type)
-- ============================================================
SELECT
    card_tier,
    COUNT(*)                                AS total_txns,
    SUM(CASE WHEN gross_amount > 15000
             THEN 1 ELSE 0 END)             AS high_value_txns,
    ROUND(
        SUM(CASE WHEN gross_amount > 15000 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    )                                       AS high_value_pct,
    ROUND(AVG(gross_amount), 2)             AS avg_txn_value,
    ROUND(SUM(gross_amount), 2)             AS total_spend
FROM transactions
WHERE is_approved = 1
GROUP BY card_tier
ORDER BY total_spend DESC;


-- ============================================================
-- Q6. Running cumulative spend per month (2024 only)
--     (Window function — SUM OVER ORDER BY)
-- ============================================================
WITH monthly_spend AS (
    SELECT
        transaction_month,
        ROUND(SUM(gross_amount), 2) AS monthly_spend
    FROM transactions
    WHERE is_approved = 1
      AND transaction_year = 2024
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
ORDER BY transaction_month;


-- ============================================================
-- Q7. Weekend vs Weekday spending behaviour
--     (Behavioural insight — product analytics)
-- ============================================================
SELECT
    CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    COUNT(*)                         AS total_transactions,
    ROUND(SUM(gross_amount), 2)      AS total_spend,
    ROUND(AVG(gross_amount), 2)      AS avg_spend,
    ROUND(SUM(cashback_amount), 2)   AS cashback_issued
FROM transactions
WHERE is_approved = 1
GROUP BY is_weekend;


-- ============================================================
-- Q8. Identify top 10 customers by total lifetime spend
--     (Customer lifetime value — CLV proxy)
-- ============================================================
SELECT
    customer_id,
    card_tier,
    city,
    COUNT(*)                        AS total_transactions,
    ROUND(SUM(gross_amount), 2)     AS lifetime_spend,
    ROUND(SUM(cashback_amount), 2)  AS total_cashback_earned,
    ROUND(AVG(gross_amount), 2)     AS avg_txn_value
FROM transactions
WHERE is_approved = 1
GROUP BY customer_id, card_tier, city
ORDER BY lifetime_spend DESC
LIMIT 10;


-- ============================================================
-- Q9. Cashback efficiency — which category gives most cashback
--     relative to spend? (ROI analysis)
-- ============================================================
SELECT
    merchant_category,
    ROUND(SUM(gross_amount), 2)                 AS total_spend,
    ROUND(SUM(cashback_amount), 2)              AS total_cashback,
    ROUND(
        SUM(cashback_amount) * 100.0
        / NULLIF(SUM(gross_amount), 0), 3
    )                                            AS cashback_yield_pct,
    COUNT(DISTINCT customer_id)                  AS unique_customers
FROM transactions
WHERE is_approved = 1
GROUP BY merchant_category
ORDER BY cashback_yield_pct DESC;


-- ============================================================
-- Q10. Quarter-on-quarter growth in transaction count
--      (QoQ analysis — executive reporting)
-- ============================================================
WITH quarterly AS (
    SELECT
        transaction_year,
        transaction_quarter,
        COUNT(*)                    AS txn_count,
        ROUND(SUM(gross_amount), 2) AS total_spend
    FROM transactions
    WHERE is_approved = 1
    GROUP BY transaction_year, transaction_quarter
)
SELECT
    transaction_year,
    transaction_quarter,
    txn_count,
    total_spend,
    LAG(txn_count) OVER (ORDER BY transaction_year, transaction_quarter)
        AS prev_quarter_count,
    ROUND(
        (txn_count - LAG(txn_count) OVER (
            ORDER BY transaction_year, transaction_quarter))
        * 100.0
        / NULLIF(LAG(txn_count) OVER (
            ORDER BY transaction_year, transaction_quarter), 0),
    2) AS qoq_growth_pct
FROM quarterly
ORDER BY transaction_year, transaction_quarter;


-- ============================================================
-- Q11. Cities with highest transaction decline rates
--      (Risk & operations monitoring)
-- ============================================================
SELECT
    city,
    COUNT(*)                                                   AS total_txns,
    SUM(CASE WHEN status = 'Declined' THEN 1 ELSE 0 END)      AS declined,
    ROUND(
        SUM(CASE WHEN status = 'Declined' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    )                                                          AS decline_rate_pct,
    ROUND(SUM(CASE WHEN status = 'Declined'
                   THEN gross_amount ELSE 0 END), 2)           AS declined_value
FROM transactions
GROUP BY city
ORDER BY decline_rate_pct DESC;


-- ============================================================
-- Q12. Online vs Offline channel spend split by card tier
--      (Multi-dimension cross tab — product manager question)
-- ============================================================
SELECT
    card_tier,
    ROUND(SUM(CASE WHEN payment_mode = 'Online'
                   THEN gross_amount ELSE 0 END), 2)      AS online_spend,
    ROUND(SUM(CASE WHEN payment_mode IN ('Swipe', 'Contactless')
                   THEN gross_amount ELSE 0 END), 2)      AS offline_spend,
    ROUND(SUM(CASE WHEN payment_mode = 'Emi'
                   THEN gross_amount ELSE 0 END), 2)      AS emi_spend,
    ROUND(SUM(gross_amount), 2)                           AS total_spend,
    ROUND(
        SUM(CASE WHEN payment_mode = 'Online'
                 THEN gross_amount ELSE 0 END)
        * 100.0 / NULLIF(SUM(gross_amount), 0), 2
    )                                                     AS online_share_pct
FROM transactions
WHERE is_approved = 1
GROUP BY card_tier
ORDER BY total_spend DESC;


-- ============================================================
-- Q13. Detect potential fraudulent pattern — customers with
--      unusually high transaction frequency on a single day
--      (Anomaly detection — risk analytics)
-- ============================================================
WITH daily_freq AS (
    SELECT
        customer_id,
        DATE(transaction_date)  AS txn_day,
        COUNT(*)                AS txns_in_day,
        SUM(gross_amount)       AS day_spend
    FROM transactions
    WHERE is_approved = 1
    GROUP BY customer_id, DATE(transaction_date)
),
avg_freq AS (
    SELECT
        customer_id,
        AVG(txns_in_day)   AS avg_daily_txns,
        MAX(txns_in_day)   AS max_daily_txns
    FROM daily_freq
    GROUP BY customer_id
)
SELECT
    d.customer_id,
    d.txn_day,
    d.txns_in_day,
    d.day_spend,
    ROUND(a.avg_daily_txns, 2) AS avg_daily_txns
FROM daily_freq d
JOIN avg_freq   a ON d.customer_id = a.customer_id
WHERE d.txns_in_day >= 4          -- threshold: 4+ txns in one day
ORDER BY d.txns_in_day DESC
LIMIT 20;


-- ============================================================
-- Q14. EMI adoption rate — which tier uses EMI most?
--      (Product feature adoption — fintech analytics)
-- ============================================================
SELECT
    card_tier,
    COUNT(*)                                                    AS total_txns,
    SUM(CASE WHEN payment_mode = 'Emi' THEN 1 ELSE 0 END)      AS emi_txns,
    ROUND(
        SUM(CASE WHEN payment_mode = 'Emi' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    )                                                           AS emi_adoption_pct,
    ROUND(
        AVG(CASE WHEN payment_mode = 'Emi'
                 THEN gross_amount END), 2
    )                                                           AS avg_emi_ticket_size
FROM transactions
WHERE is_approved = 1
GROUP BY card_tier
ORDER BY emi_adoption_pct DESC;


-- ============================================================
-- Q15. Full customer scorecard — top 20 customers ranked by
--      composite score (spend + frequency + low decline rate)
--      (Executive dashboard KPI — senior analyst question)
-- ============================================================
WITH customer_stats AS (
    SELECT
        customer_id,
        card_tier,
        city,
        COUNT(*)                                             AS total_txns,
        ROUND(SUM(gross_amount), 2)                         AS total_spend,
        ROUND(AVG(gross_amount), 2)                         AS avg_spend,
        SUM(CASE WHEN status = 'Declined' THEN 1 ELSE 0 END) AS declines,
        ROUND(
            SUM(CASE WHEN status = 'Declined' THEN 1 ELSE 0 END)
            * 100.0 / COUNT(*), 2
        )                                                    AS decline_rate_pct,
        ROUND(SUM(cashback_amount), 2)                       AS total_cashback
    FROM transactions
    GROUP BY customer_id, card_tier, city
),
scored AS (
    SELECT *,
        ROUND(
            (total_spend / 10000.0)
          + (total_txns  * 2.0)
          - (decline_rate_pct * 5.0),
        2) AS customer_score
    FROM customer_stats
)
SELECT
    customer_id, card_tier, city,
    total_txns, total_spend, avg_spend,
    decline_rate_pct, total_cashback,
    customer_score,
    RANK() OVER (ORDER BY customer_score DESC) AS score_rank
FROM scored
ORDER BY customer_score DESC
LIMIT 20;
