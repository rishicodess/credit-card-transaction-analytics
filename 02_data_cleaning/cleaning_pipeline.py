"""
========================================================
  Data Cleaning & Exploratory Data Analysis
  Author  : Rishabh Gupta
  Domain  : BFSI – Credit Card Transaction Analytics
  Input   : data/raw/transactions.csv
  Output  : data/processed/transactions_clean.csv
========================================================

STEPS COVERED
─────────────
  1. Load raw data & initial inspection
  2. Handle missing values
  3. Fix data types
  4. Remove duplicates
  5. Derive business metrics
  6. Detect & flag outliers
  7. Export cleaned dataset
  8. EDA visualizations (saved as PNG)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────
BASE      = os.path.join(os.path.dirname(__file__), "..")
RAW_PATH  = os.path.join(BASE, "data", "raw",       "transactions.csv")
OUT_PATH  = os.path.join(BASE, "data", "processed", "transactions_clean.csv")
CHART_DIR = os.path.join(BASE, "04_dashboard", "eda_charts")
os.makedirs(CHART_DIR, exist_ok=True)

# ── Plot style ────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="Blues_d")
BRAND_COLOR = "#1A3C5E"   # deep navy — BFSI feel

# ══════════════════════════════════════════════════════
# STEP 1 — Load & Inspect
# ══════════════════════════════════════════════════════
print("\n" + "="*55)
print("  STEP 1 — Load & Initial Inspection")
print("="*55)

df = pd.read_csv(RAW_PATH)

print(f"\n  Shape         : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"  Memory usage  : {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
print(f"\n  Column types:\n{df.dtypes.to_string()}")
print(f"\n  Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string()}")
print(f"\n  Duplicates    : {df.duplicated().sum()}")

# ══════════════════════════════════════════════════════
# STEP 2 — Fix Data Types
# ══════════════════════════════════════════════════════
print("\n" + "="*55)
print("  STEP 2 — Fix Data Types")
print("="*55)

df["transaction_date"] = pd.to_datetime(df["transaction_date"])

# Standardise string columns
str_cols = ["merchant_category", "card_tier", "city",
            "payment_mode", "status", "day_of_week"]
for col in str_cols:
    df[col] = df[col].astype(str).str.strip().str.title()

print("  ✓ transaction_date  → datetime")
print("  ✓ string columns    → stripped & title-cased")

# ══════════════════════════════════════════════════════
# STEP 3 — Handle Missing Values
# ══════════════════════════════════════════════════════
print("\n" + "="*55)
print("  STEP 3 — Handle Missing Values")
print("="*55)

before = df.isnull().sum().sum()

# merchant_category nulls → "Unclassified" (business rule)
df["merchant_category"] = df["merchant_category"].replace("Nan", np.nan)
null_merchant = df["merchant_category"].isnull().sum()
df["merchant_category"].fillna("Unclassified", inplace=True)

after = df.isnull().sum().sum()
print(f"  merchant_category nulls filled : {null_merchant}")
print(f"  Total nulls before             : {before}")
print(f"  Total nulls after              : {after}")

# ══════════════════════════════════════════════════════
# STEP 4 — Remove Duplicates
# ══════════════════════════════════════════════════════
print("\n" + "="*55)
print("  STEP 4 — Remove Duplicates")
print("="*55)

dupes = df.duplicated(subset="transaction_id").sum()
df.drop_duplicates(subset="transaction_id", inplace=True)
print(f"  Duplicate transaction_ids removed : {dupes}")
print(f"  Clean shape                       : {df.shape}")

# ══════════════════════════════════════════════════════
# STEP 5 — Derive Business Metrics
# ══════════════════════════════════════════════════════
print("\n" + "="*55)
print("  STEP 5 — Derive Business Metrics")
print("="*55)

# Utilisation ratio (transaction vs credit limit — proxy)
df["utilisation_flag"] = (
    df["gross_amount"] > df["credit_limit"] * 0.30
).astype(int)

# Transaction size bucket
bins   = [0, 1_000, 5_000, 15_000, 50_000, float("inf")]
labels = ["Micro (<1K)", "Small (1K-5K)", "Medium (5K-15K)",
          "Large (15K-50K)", "High Value (>50K)"]
df["txn_size_bucket"] = pd.cut(
    df["gross_amount"], bins=bins, labels=labels
)

# Weekend flag
df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"]).astype(int)

# Approved only flag
df["is_approved"] = (df["status"] == "Approved").astype(int)

print("  ✓ utilisation_flag   — high-spend relative to limit")
print("  ✓ txn_size_bucket    — Micro / Small / Medium / Large / High Value")
print("  ✓ is_weekend         — 1 if Saturday or Sunday")
print("  ✓ is_approved        — 1 if status = Approved")

# ══════════════════════════════════════════════════════
# STEP 6 — Outlier Detection (IQR method)
# ══════════════════════════════════════════════════════
print("\n" + "="*55)
print("  STEP 6 — Outlier Detection (gross_amount)")
print("="*55)

Q1  = df["gross_amount"].quantile(0.25)
Q3  = df["gross_amount"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df["is_outlier"] = (
    (df["gross_amount"] < lower_bound) |
    (df["gross_amount"] > upper_bound)
).astype(int)

n_outliers = df["is_outlier"].sum()
print(f"  IQR range    : ₹{lower_bound:,.0f} — ₹{upper_bound:,.0f}")
print(f"  Outliers     : {n_outliers} ({n_outliers/len(df)*100:.1f}%)")
print("  NOTE: Outliers are FLAGGED, not removed (valid high-value txns)")

# ══════════════════════════════════════════════════════
# STEP 7 — Export Cleaned Dataset
# ══════════════════════════════════════════════════════
print("\n" + "="*55)
print("  STEP 7 — Export Clean Dataset")
print("="*55)

df.to_csv(OUT_PATH, index=False)
print(f"  ✅ Saved → {OUT_PATH}")
print(f"     Rows    : {len(df):,}")
print(f"     Columns : {len(df.columns)}")

# ══════════════════════════════════════════════════════
# STEP 8 — EDA Visualizations
# ══════════════════════════════════════════════════════
print("\n" + "="*55)
print("  STEP 8 — EDA Visualizations")
print("="*55)

approved = df[df["is_approved"] == 1].copy()

# ── Chart 1: Monthly Transaction Volume ──────────────
fig, ax = plt.subplots(figsize=(12, 4))
monthly = (approved.groupby(["transaction_year", "transaction_month"])
           ["gross_amount"].sum().reset_index())
monthly["period"] = (monthly["transaction_year"].astype(str) + "-"
                     + monthly["transaction_month"].astype(str).str.zfill(2))
monthly = monthly.sort_values("period")
ax.bar(monthly["period"], monthly["gross_amount"] / 1e5,
       color=BRAND_COLOR, alpha=0.85, edgecolor="white")
ax.set_title("Monthly Transaction Volume (₹ Lakhs)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Gross Amount (₹ Lakhs)")
plt.xticks(rotation=45, ha="right", fontsize=7)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"₹{x:.0f}L"))
plt.tight_layout()
p = os.path.join(CHART_DIR, "01_monthly_volume.png")
plt.savefig(p, dpi=150); plt.close()
print(f"  ✓ Saved: {p}")

# ── Chart 2: Spend by Merchant Category ──────────────
fig, ax = plt.subplots(figsize=(9, 5))
cat_spend = (approved.groupby("merchant_category")
             ["gross_amount"].sum().sort_values(ascending=True))
colors = sns.color_palette("Blues_d", len(cat_spend))
cat_spend.plot(kind="barh", ax=ax, color=colors, edgecolor="white")
ax.set_title("Total Spend by Merchant Category",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Gross Amount (₹)")
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
plt.tight_layout()
p = os.path.join(CHART_DIR, "02_category_spend.png")
plt.savefig(p, dpi=150); plt.close()
print(f"  ✓ Saved: {p}")

# ── Chart 3: Card Tier Distribution ──────────────────
fig, ax = plt.subplots(figsize=(7, 5))
tier_counts = approved["card_tier"].value_counts()
tier_counts.plot(kind="bar", ax=ax,
                 color=sns.color_palette("Blues_d", len(tier_counts)),
                 edgecolor="white")
ax.set_title("Transaction Count by Card Tier",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Card Tier"); ax.set_ylabel("Number of Transactions")
plt.xticks(rotation=0)
plt.tight_layout()
p = os.path.join(CHART_DIR, "03_card_tier.png")
plt.savefig(p, dpi=150); plt.close()
print(f"  ✓ Saved: {p}")

# ── Chart 4: Avg Spend by City ────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
city_avg = (approved.groupby("city")["gross_amount"]
            .mean().sort_values(ascending=False))
city_avg.plot(kind="bar", ax=ax,
              color=BRAND_COLOR, alpha=0.85, edgecolor="white")
ax.set_title("Average Transaction Value by City",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("City"); ax.set_ylabel("Avg Gross Amount (₹)")
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
p = os.path.join(CHART_DIR, "04_city_avg_spend.png")
plt.savefig(p, dpi=150); plt.close()
print(f"  ✓ Saved: {p}")

# ── Chart 5: Payment Mode Share ───────────────────────
fig, ax = plt.subplots(figsize=(6, 6))
mode_counts = approved["payment_mode"].value_counts()
wedge_props = {"edgecolor": "white", "linewidth": 2}
ax.pie(mode_counts, labels=mode_counts.index, autopct="%1.1f%%",
       colors=sns.color_palette("Blues_d", len(mode_counts)),
       wedgeprops=wedge_props, startangle=140)
ax.set_title("Payment Mode Distribution",
             fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
p = os.path.join(CHART_DIR, "05_payment_mode.png")
plt.savefig(p, dpi=150); plt.close()
print(f"  ✓ Saved: {p}")

# ── Chart 6: Transaction Size Buckets ────────────────
fig, ax = plt.subplots(figsize=(9, 4))
bucket_counts = (approved["txn_size_bucket"]
                 .value_counts()
                 .reindex(labels))
bucket_counts.plot(kind="bar", ax=ax,
                   color=sns.color_palette("Blues_d", len(labels)),
                   edgecolor="white")
ax.set_title("Transaction Volume by Size Bucket",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Transaction Size"); ax.set_ylabel("Count")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
p = os.path.join(CHART_DIR, "06_txn_size_buckets.png")
plt.savefig(p, dpi=150); plt.close()
print(f"  ✓ Saved: {p}")

print("\n  ✅ All EDA charts saved to 04_dashboard/eda_charts/")
print("\n" + "="*55)
print("  Cleaning pipeline complete!")
print("="*55 + "\n")
