import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

st.title("📈 Financial Analytics")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/transactions.csv")
df["date"] = pd.to_datetime(df["date"])

expenses = df[df["amount"] < 0].copy()
expenses["amount"] = expenses["amount"].abs()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

categories = sorted(expenses["ground_truth_category"].unique())

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + categories
)

if selected_category != "All":
    expenses = expenses[
        expenses["ground_truth_category"] == selected_category
    ]

# -----------------------------
# KPI Cards
# -----------------------------
total_spent = expenses["amount"].sum()
avg_transaction = expenses["amount"].mean()
largest_transaction = expenses["amount"].max()
num_transactions = len(expenses)

c1, c2, c3, c4 = st.columns(4)

c1.metric("💸 Total Spent", f"₹{total_spent:,.0f}")
c2.metric("💳 Avg Transaction", f"₹{avg_transaction:,.0f}")
c3.metric("🔥 Largest Expense", f"₹{largest_transaction:,.0f}")
c4.metric("🧾 Transactions", num_transactions)

st.divider()

# -----------------------------
# Monthly Spending
# -----------------------------
monthly = (
    expenses
    .groupby(expenses["date"].dt.to_period("M"))["amount"]
    .sum()
    .reset_index()
)

monthly["date"] = monthly["date"].astype(str)

fig = px.line(
    monthly,
    x="date",
    y="amount",
    markers=True,
    title="Monthly Spending Trend"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Category Spending
# -----------------------------
left, right = st.columns(2)

category = (
    expenses
    .groupby("ground_truth_category")["amount"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    category,
    values="amount",
    names="ground_truth_category",
    title="Category-wise Spending"
)

left.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Top Merchants
# -----------------------------
merchant = (
    expenses
    .groupby("merchant")["amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    merchant,
    x="merchant",
    y="amount",
    title="Top 10 Merchants"
)

right.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Daily Spending
# -----------------------------
daily = (
    expenses
    .groupby(expenses["date"].dt.date)["amount"]
    .sum()
    .reset_index()
)

fig4 = px.area(
    daily,
    x="date",
    y="amount",
    title="Daily Spending"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Largest Transactions
# -----------------------------
st.subheader("🏆 Top 10 Largest Transactions")

largest = (
    expenses
    .sort_values("amount", ascending=False)
    .head(10)
)

st.dataframe(
    largest[
        [
            "date",
            "merchant",
            "ground_truth_category",
            "amount"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# Financial Insights
# -----------------------------
st.subheader("💡 AI Financial Insights")

highest_category = category.sort_values(
    "amount",
    ascending=False
).iloc[0]

highest_merchant = merchant.iloc[0]

st.success(
    f"""
• Highest spending category: **{highest_category['ground_truth_category']}**

• Amount spent: **₹{highest_category['amount']:,.0f}**

• Highest spending merchant: **{highest_merchant['merchant']}**

• Merchant spend: **₹{highest_merchant['amount']:,.0f}**
"""
)