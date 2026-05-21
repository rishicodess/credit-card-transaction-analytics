"""
========================================================
  Credit Card Transaction Dataset Generator
  Author  : Rishabh Gupta
  Domain  : BFSI – Transaction Analytics
  Purpose : Generate realistic synthetic credit card
            transaction data for portfolio analysis
========================================================
"""

import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

# ── Reproducibility ───────────────────────────────────
np.random.seed(42)
random.seed(42)

# ── Config ────────────────────────────────────────────
N_CUSTOMERS    = 1_000
N_TRANSACTIONS = 15_000
START_DATE     = datetime(2023, 1, 1)
END_DATE       = datetime(2024, 12, 31)
OUTPUT_PATH    = os.path.join(os.path.dirname(__file__),
                              "..", "data", "raw", "transactions.csv")

# ── Reference Data ────────────────────────────────────
CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"
]

CARD_TIERS = {
    "Classic" : 0.45,   # proportion of customers
    "Gold"    : 0.30,
    "Platinum": 0.20,
    "Infinite": 0.05,
}

MERCHANT_CATEGORIES = {
    "Grocery"         : {"avg": 2_500,  "std": 1_200, "weight": 0.22},
    "Dining"          : {"avg": 1_800,  "std":   900, "weight": 0.18},
    "Travel"          : {"avg": 12_000, "std": 6_000, "weight": 0.10},
    "Electronics"     : {"avg": 18_000, "std": 9_000, "weight": 0.08},
    "Healthcare"      : {"avg": 3_500,  "std": 2_000, "weight": 0.10},
    "Fuel"            : {"avg": 2_200,  "std":   800, "weight": 0.12},
    "Entertainment"   : {"avg": 1_500,  "std":   700, "weight": 0.08},
    "Online Shopping" : {"avg": 4_500,  "std": 2_500, "weight": 0.12},
}

CASHBACK_BY_TIER = {
    "Classic" : 0.005,
    "Gold"    : 0.010,
    "Platinum": 0.015,
    "Infinite": 0.020,
}

CREDIT_LIMIT_BY_TIER = {
    "Classic" : (50_000,  1_50_000),
    "Gold"    : (1_50_000, 3_00_000),
    "Platinum": (3_00_000, 6_00_000),
    "Infinite": (6_00_000, 15_00_000),
}

STATUS_WEIGHTS = [0.78, 0.12, 0.10]   # Active / Dormant / Delinquent

# ── Build Customers ───────────────────────────────────
print("▶ Generating customer master...")

tiers = np.random.choice(
    list(CARD_TIERS.keys()),
    size=N_CUSTOMERS,
    p=list(CARD_TIERS.values())
)

customers = pd.DataFrame({
    "customer_id"  : [f"CUST{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS + 1)],
    "card_tier"    : tiers,
    "city"         : np.random.choice(CITIES, size=N_CUSTOMERS),
    "account_status": np.random.choice(
        ["Active", "Dormant", "Delinquent"],
        size=N_CUSTOMERS,
        p=STATUS_WEIGHTS
    ),
})

customers["credit_limit"] = customers["card_tier"].apply(
    lambda t: random.randint(*CREDIT_LIMIT_BY_TIER[t])
)
customers["cashback_rate"] = customers["card_tier"].map(CASHBACK_BY_TIER)

# ── Build Transactions ────────────────────────────────
print("▶ Generating transactions...")

# Only Active customers transact (dormant/delinquent occasionally do)
active_custs = customers[customers["account_status"] == "Active"]["customer_id"].tolist()
other_custs  = customers[customers["account_status"] != "Active"]["customer_id"].tolist()

sampled_customers = (
    random.choices(active_custs, k=int(N_TRANSACTIONS * 0.90)) +
    random.choices(other_custs,  k=int(N_TRANSACTIONS * 0.10))
)
random.shuffle(sampled_customers)

categories = list(MERCHANT_CATEGORIES.keys())
cat_weights = [MERCHANT_CATEGORIES[c]["weight"] for c in categories]

txn_categories = np.random.choice(categories, size=N_TRANSACTIONS, p=cat_weights)

# Random timestamps spread across date range
delta_days = (END_DATE - START_DATE).days
txn_dates  = [
    START_DATE + timedelta(
        days=random.randint(0, delta_days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    for _ in range(N_TRANSACTIONS)
]

# Gross amounts based on merchant category
gross_amounts = np.array([
    max(100, np.random.normal(
        MERCHANT_CATEGORIES[c]["avg"],
        MERCHANT_CATEGORIES[c]["std"]
    ))
    for c in txn_categories
])
gross_amounts = np.round(gross_amounts, 2)

transactions = pd.DataFrame({
    "transaction_id"     : [f"TXN{str(i).zfill(7)}" for i in range(1, N_TRANSACTIONS + 1)],
    "customer_id"        : sampled_customers[:N_TRANSACTIONS],
    "transaction_date"   : txn_dates,
    "merchant_category"  : txn_categories,
    "gross_amount"       : gross_amounts,
    "city"               : np.random.choice(CITIES, size=N_TRANSACTIONS),
    "payment_mode"       : np.random.choice(
        ["Swipe", "Online", "Contactless", "EMI"],
        size=N_TRANSACTIONS,
        p=[0.30, 0.40, 0.20, 0.10]
    ),
    "status"             : np.random.choice(
        ["Approved", "Declined", "Reversed"],
        size=N_TRANSACTIONS,
        p=[0.92, 0.05, 0.03]
    ),
})

# ── Derived Columns ───────────────────────────────────
transactions = transactions.merge(
    customers[["customer_id", "card_tier", "cashback_rate", "credit_limit"]],
    on="customer_id",
    how="left"
)

transactions["cashback_amount"] = (
    transactions["gross_amount"] * transactions["cashback_rate"]
).round(2)

transactions["net_transaction"] = (
    transactions["gross_amount"] - transactions["cashback_amount"]
).round(2)

transactions["transaction_year"]  = pd.DatetimeIndex(transactions["transaction_date"]).year
transactions["transaction_month"] = pd.DatetimeIndex(transactions["transaction_date"]).month
transactions["transaction_quarter"] = pd.DatetimeIndex(transactions["transaction_date"]).quarter
transactions["day_of_week"] = pd.DatetimeIndex(transactions["transaction_date"]).day_name()

# ── Introduce Realistic Nulls ─────────────────────────
null_idx = transactions.sample(frac=0.02).index
transactions.loc[null_idx, "merchant_category"] = np.nan

# ── Save ──────────────────────────────────────────────
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
transactions.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Dataset saved  → {OUTPUT_PATH}")
print(f"   Rows           : {len(transactions):,}")
print(f"   Columns        : {len(transactions.columns)}")
print(f"   Date range     : {transactions['transaction_date'].min()} "
      f"→ {transactions['transaction_date'].max()}")
print(f"   Total spend    : ₹{transactions['gross_amount'].sum():,.0f}")
