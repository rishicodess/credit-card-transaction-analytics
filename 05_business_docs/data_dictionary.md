# Data Dictionary
### Credit Card Transaction Analytics Dataset
**Author:** Rishabh Gupta

---

## Table: transactions

| Column               | Type    | Description                                                       | Example              |
|----------------------|---------|-------------------------------------------------------------------|----------------------|
| transaction_id       | TEXT    | Unique identifier for each transaction                            | TXN0000001           |
| customer_id          | TEXT    | Unique identifier for each cardholder                             | CUST00042            |
| transaction_date     | DATETIME| Date and time of transaction                                      | 2023-03-15 14:32:00  |
| merchant_category    | TEXT    | Business category of the merchant                                 | Electronics          |
| gross_amount         | REAL    | Full transaction amount before cashback (INR)                     | 18500.00             |
| city                 | TEXT    | City where transaction was initiated                              | Bengaluru            |
| payment_mode         | TEXT    | Channel used: Swipe / Online / Contactless / EMI                  | Online               |
| status               | TEXT    | Transaction outcome: Approved / Declined / Reversed               | Approved             |
| card_tier            | TEXT    | Customer card tier: Classic / Gold / Platinum / Infinite          | Platinum             |
| cashback_rate        | REAL    | Cashback percentage applicable to the card tier (decimal)         | 0.015                |
| credit_limit         | INTEGER | Total sanctioned credit limit for the customer (INR)              | 400000               |
| cashback_amount      | REAL    | Cashback amount credited = gross_amount × cashback_rate           | 277.50               |
| net_transaction      | REAL    | Effective amount = gross_amount − cashback_amount                 | 18222.50             |
| transaction_year     | INTEGER | Calendar year extracted from transaction_date                     | 2023                 |
| transaction_month    | INTEGER | Calendar month (1–12) extracted from transaction_date             | 3                    |
| transaction_quarter  | INTEGER | Calendar quarter (1–4) extracted from transaction_date            | 1                    |
| day_of_week          | TEXT    | Day name extracted from transaction_date                          | Wednesday            |
| utilisation_flag     | INTEGER | 1 if gross_amount > 30% of credit_limit, else 0                   | 0                    |
| txn_size_bucket      | TEXT    | Spend tier: Micro / Small / Medium / Large / High Value           | Large (15K-50K)      |
| is_weekend           | INTEGER | 1 if transaction on Saturday or Sunday, else 0                    | 0                    |
| is_approved          | INTEGER | 1 if status = Approved, else 0                                    | 1                    |
| is_outlier           | INTEGER | 1 if gross_amount outside IQR 1.5× bounds, else 0                 | 0                    |

---

## Merchant Categories

| Category         | Avg Ticket Size | Description                                   |
|------------------|-----------------|-----------------------------------------------|
| Grocery          | ₹2,500          | Supermarkets, kirana stores, food retail       |
| Dining           | ₹1,800          | Restaurants, cafes, food delivery              |
| Travel           | ₹12,000         | Airlines, hotels, cabs, railway bookings       |
| Electronics      | ₹18,000         | Consumer electronics, appliances, gadgets      |
| Healthcare       | ₹3,500          | Hospitals, pharmacies, diagnostics             |
| Fuel             | ₹2,200          | Petrol pumps, CNG stations                     |
| Entertainment    | ₹1,500          | Multiplex, OTT subscriptions, gaming           |
| Online Shopping  | ₹4,500          | E-commerce platforms (Amazon, Flipkart, etc.)  |

---

## Card Tier Reference

| Tier     | Customer Share | Cashback Rate | Credit Limit Range    |
|----------|----------------|---------------|-----------------------|
| Classic  | 45%            | 0.5%          | ₹50,000 – ₹1,50,000  |
| Gold     | 30%            | 1.0%          | ₹1,50,000 – ₹3,00,000|
| Platinum | 20%            | 1.5%          | ₹3,00,000 – ₹6,00,000|
| Infinite | 5%             | 2.0%          | ₹6,00,000 – ₹15,00,000|
