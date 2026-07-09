import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Transaction Explorer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Transaction Explorer")

# ------------------------------------
# Load Dataset
# ------------------------------------

df = pd.read_csv("data/transactions.csv")
df["date"] = pd.to_datetime(df["date"])

# ------------------------------------
# Sidebar Filters
# ------------------------------------

st.sidebar.header("Filters")

# Date Filter
min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Category Filter
categories = sorted(df["ground_truth_category"].unique())

selected_category = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

# Merchant Filter
merchants = sorted(df["merchant"].unique())

selected_merchants = st.sidebar.multiselect(
    "Merchant",
    merchants,
    default=merchants
)

# Amount Filter
amount_range = st.sidebar.slider(
    "Transaction Amount (₹)",
    0,
    int(df["amount"].abs().max()),
    (0, int(df["amount"].abs().max()))
)

# ------------------------------------
# Search
# ------------------------------------

search = st.text_input(
    "Search Transaction Description"
)

# ------------------------------------
# Apply Filters
# ------------------------------------

filtered = df.copy()

# Date Filter
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[
        (filtered["date"] >= start) &
        (filtered["date"] <= end)
    ]

# Category
filtered = filtered[
    filtered["ground_truth_category"].isin(selected_category)
]

# Merchant
filtered = filtered[
    filtered["merchant"].isin(selected_merchants)
]

# Amount
filtered = filtered[
    filtered["amount"].abs().between(
        amount_range[0],
        amount_range[1]
    )
]

# Search
if search:

    filtered = filtered[
        filtered["description"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ------------------------------------
# KPI Cards
# ------------------------------------

st.subheader("Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Transactions",
    len(filtered)
)

c2.metric(
    "Total Expenses",
    f"₹{-filtered[filtered.amount<0]['amount'].sum():,.0f}"
)

c3.metric(
    "Total Income",
    f"₹{filtered[filtered.amount>0]['amount'].sum():,.0f}"
)

st.divider()

# ------------------------------------
# Transactions Table
# ------------------------------------

st.subheader("Transactions")

st.dataframe(
    filtered.sort_values(
        "date",
        ascending=False
    ),
    use_container_width=True,
    height=500
)

# ------------------------------------
# Download
# ------------------------------------

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Transactions",
    csv,
    file_name="filtered_transactions.csv",
    mime="text/csv"
)

# ------------------------------------
# Statistics
# ------------------------------------

st.divider()

st.subheader("Statistics")

col1, col2 = st.columns(2)

with col1:

    st.write("Expense by Category")

    expense = (
        filtered[
            filtered["amount"] < 0
        ]
        .groupby("ground_truth_category")["amount"]
        .sum()
        .abs()
    )

    st.dataframe(expense)

with col2:

    st.write("Top 10 Merchants")

    merchants = (
        filtered[
            filtered["amount"] < 0
        ]
        .groupby("merchant")["amount"]
        .sum()
        .abs()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    st.dataframe(merchants)