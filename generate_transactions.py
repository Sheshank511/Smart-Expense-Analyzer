"""
Synthetic Transaction Data Generator
-------------------------------------
Generates realistic Indian bank-statement-style transactions for the
Smart Expense Analyzer project.

Why synthetic data instead of a public dataset?
Real bank statements can't be shared for privacy reasons, so we simulate
transactions with the same messy characteristics real statements have:
inconsistent merchant string formats, UPI reference noise, recurring
patterns (salary, rent, bills), and injected anomalies for fraud detection.

import argparse
import random
import string
from datetime import date, timedelta

import pandas as pd

random.seed(42)

# ---------------------------------------------------------------------------
# 1. Category -> merchant pool, with typical amount ranges (INR)
#    ground_truth_category is kept ONLY for training/evaluating the
#    categorizer later -- your model should predict it from `description`.
# ---------------------------------------------------------------------------
CATEGORIES = {
    "Food & Dining": {
        "merchants": ["Swiggy", "Zomato", "Dominos", "McDonalds", "Chai Point",
                      "Behrouz Biryani", "Faasos", "Starbucks", "Local Tiffin Center"],
        "amount_range": (80, 900),
        "freq_per_month": (7, 12),  # roughly daily-ish
    },
    "Groceries": {
        "merchants": ["BigBasket", "Blinkit", "Zepto", "DMart", "Reliance Fresh",
                      "Local Kirana Store"],
        "amount_range": (150, 2500),
        "freq_per_month": (4, 8),
    },
    "Travel & Transport": {
        "merchants": ["Uber", "Ola Cabs", "IRCTC", "RedBus", "Rapido",
                      "Indian Oil Petrol Pump", "Metro Rail Recharge"],
        "amount_range": (30, 2000),
        "freq_per_month": (6, 10),
    },
    "Bills & Utilities": {
        "merchants": ["Airtel Postpaid", "Jio Fiber", "TSSPDCL Electricity",
                      "Water Board", "Tata Sky", "Google Play Recharge"],
        "amount_range": (200, 1800),
        "freq_per_month": (2, 5),
    },
    "Shopping": {
        "merchants": ["Amazon", "Flipkart", "Myntra", "Ajio", "Croma", "Decathlon"],
        "amount_range": (300, 5000),
        "freq_per_month": (2, 6),
    },
    "Entertainment": {
        "merchants": ["Netflix", "Spotify Premium", "BookMyShow", "PVR Cinemas",
                      "Amazon Prime Video", "Hotstar"],
        "amount_range": (100, 900),
        "freq_per_month": (2, 5),
    },
    "Healthcare": {
        "merchants": ["Apollo Pharmacy", "PharmEasy", "1mg", "Practo Consultation",
                      "Local Clinic"],
        "amount_range": (100, 2500),
        "freq_per_month": (1, 4),
    },
    "Education": {
        "merchants": ["Udemy", "Coursera", "GeeksforGeeks Practice", "NIT Warangal Mess Fee",
                      "Byju's", "Local Xerox and Stationery"],
        "amount_range": (100, 2500),
        "freq_per_month": (1, 2),
    },
    "Miscellaneous": {
        "merchants": ["ATM Withdrawal", "IMPS Transfer", "Google Pay Send",
                      "PhonePe Send", "Salon and Grooming"],
        "amount_range": (100, 2000),
        "freq_per_month": (2, 6),
    },
}

# Fixed monthly transactions (income + rent) -- these anchor realistic cashflow
RENT_AMOUNT_RANGE = (7000, 12000)
SALARY_AMOUNT_RANGE = (0, 0)  # set via --stipend flag if user has income; students often skip

# Different banks format UPI/merchant strings differently -- simulate that noise
STRING_TEMPLATES = [
    "UPI-{merchant}-{ref}@okhdfcbank",
    "UPI/{merchant}/{ref}/Payment",
    "POS {merchant} {ref}",
    "{merchant}",
    "NEFT-{merchant}-{ref}",
    "IMPS/{ref}/{merchant}",
    "{merchant} PVT LTD {ref}",
]


def random_ref(n=6):
    return "".join(random.choices(string.digits, k=n))


def messy_description(merchant: str) -> str:
    """Turn a clean merchant name into a realistic noisy bank statement string."""
    template = random.choice(STRING_TEMPLATES)
    desc = template.format(merchant=merchant.upper().replace(" ", ""), ref=random_ref())
    # occasionally add random case noise, real statements are inconsistent
    if random.random() < 0.3:
        desc = desc.lower()
    return desc


def generate_month_transactions(year: int, month: int, include_rent: bool = True):
    """Generate all transactions for a single month."""
    rows = []
    days_in_month = (date(year, month % 12 + 1, 1) - timedelta(days=1)).day \
        if month != 12 else 31

    # Rent -- almost always on 1st-3rd
    if include_rent:
        rent_day = random.randint(1, 3)
        rows.append({
            "date": date(year, month, rent_day),
            "merchant": "House Rent Owner Transfer",
            "description": messy_description("House Rent Owner Transfer"),
            "amount": -round(random.uniform(*RENT_AMOUNT_RANGE), 2),
            "ground_truth_category": "Bills & Utilities",
        })

    # Regular category-based spends
    for category, cfg in CATEGORIES.items():
        n_txns = random.randint(*cfg["freq_per_month"])
        for _ in range(n_txns):
            day = random.randint(1, days_in_month)
            merchant = random.choice(cfg["merchants"])
            amount = round(random.uniform(*cfg["amount_range"]), 2)
            rows.append({
                "date": date(year, month, day),
                "merchant": merchant,
                "description": messy_description(merchant),
                "amount": -amount,
                "ground_truth_category": category,
            })

    return rows


def inject_anomalies(rows, n_anomalies=3):
    """
    Seed a few unusual transactions for the anomaly-detection module:
    - unusually large one-off purchase
    - odd-hour / duplicate-looking rapid transactions
    - a round-number suspicious transfer
    """
    anomaly_rows = []
    dates_available = [r["date"] for r in rows]
    if not dates_available:
        return anomaly_rows

    for _ in range(n_anomalies):
        d = random.choice(dates_available)
        kind = random.choice(["large_purchase", "duplicate_burst", "round_transfer"])

        if kind == "large_purchase":
            merchant = random.choice(["Croma", "Amazon", "Apple Store"])
            anomaly_rows.append({
                "date": d,
                "merchant": merchant,
                "description": messy_description(merchant),
                "amount": -round(random.uniform(25000, 60000), 2),
                "ground_truth_category": "Shopping",
            })
        elif kind == "duplicate_burst":
            merchant = "UNKNOWN MERCHANT"
            amt = round(random.uniform(500, 2000), 2)
            for _ in range(3):
                anomaly_rows.append({
                    "date": d,
                    "merchant": merchant,
                    "description": messy_description(merchant),
                    "amount": -amt,
                    "ground_truth_category": "Miscellaneous",
                })
        else:  # round_transfer
            merchant = "IMPS Transfer"
            anomaly_rows.append({
                "date": d,
                "merchant": merchant,
                "description": messy_description(merchant),
                "amount": -float(random.choice([10000, 15000, 20000, 25000])),
                "ground_truth_category": "Miscellaneous",
            })

    return anomaly_rows


def generate_dataset(months: int, monthly_income: float, start_year=2025, start_month=7):
    all_rows = []
    year, month = start_year, start_month

    for i in range(months):
        month_rows = generate_month_transactions(year, month)

        # Optional monthly income credit (e.g., stipend/salary)
        if monthly_income > 0:
            month_rows.append({
                "date": date(year, month, random.choice([1, 2])),
                "merchant": "Salary Credit NIT Stipend",
                "description": messy_description("Salary Credit NIT Stipend"),
                "amount": round(monthly_income, 2),
                "ground_truth_category": "Income",
            })

        all_rows.extend(month_rows)

        month += 1
        if month > 12:
            month = 1
            year += 1

    
    all_rows.extend(inject_anomalies(all_rows, n_anomalies=max(3, months // 2)))

    df = pd.DataFrame(all_rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["transaction_id"] = ["TXN{:06d}".format(i + 1) for i in range(len(df))]
    df = df[["transaction_id", "date", "merchant", "description", "amount", "ground_truth_category"]]
    return df


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic bank transaction data.")
    parser.add_argument("--months", type=int, default=12, help="Number of months of data to generate")
    parser.add_argument("--stipend", type=float, default=0.0,
                         help="Optional recurring monthly income/stipend amount (0 = skip)")
    parser.add_argument("--out", type=str, default="transactions.csv", help="Output CSV path")
    args = parser.parse_args()

    df = generate_dataset(months=args.months, monthly_income=args.stipend)
    df.to_csv(args.out, index=False)

    print(f"Generated {len(df)} transactions across {args.months} months -> {args.out}")
    print("\nCategory distribution:")
    print(df["ground_truth_category"].value_counts())
    print("\nSample rows:")
    print(df.head(8).to_string(index=False))


if __name__ == "__main__":
    main()
