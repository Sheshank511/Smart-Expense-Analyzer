import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Dashboard")

# Load Data
df = pd.read_csv("data/transactions.csv")
df["date"] = pd.to_datetime(df["date"])

# KPIs
income = df[df["amount"] > 0]["amount"].sum()
expenses = -df[df["amount"] < 0]["amount"].sum()
savings = income - expenses
transactions = len(df)

try:
    fraud = pd.read_csv("data/fraud_report.csv")
    fraud_count = len(fraud)
except:
    fraud_count = 0

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Income", f"₹{income:,.0f}")
c2.metric("💸 Expenses", f"₹{expenses:,.0f}")
c3.metric("🏦 Savings", f"₹{savings:,.0f}")
c4.metric("🚨 Fraud Alerts", fraud_count)
c5.metric("📝 Transactions", transactions)

st.divider()

left, right = st.columns(2)

# Pie Chart
category = (
    df[df["amount"] < 0]
    .groupby("ground_truth_category")["amount"]
    .sum()
    .abs()
    .reset_index()
)

fig1 = px.pie(
    category,
    values="amount",
    names="ground_truth_category",
    title="Category-wise Spending"
)

left.plotly_chart(fig1, use_container_width=True)

# Monthly Spending
monthly = (
    df[df["amount"] < 0]
    .groupby(df["date"].dt.to_period("M"))["amount"]
    .sum()
    .abs()
    .reset_index()
)

monthly["date"] = monthly["date"].astype(str)

fig2 = px.bar(
    monthly,
    x="date",
    y="amount",
    title="Monthly Spending"
)

right.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("🏪 Top 10 Merchants")

merchants = (
    df[df["amount"] < 0]
    .groupby("merchant")["amount"]
    .sum()
    .abs()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(merchants, use_container_width=True)

st.divider()

st.subheader("💡 Financial Insights")

highest = category.sort_values("amount", ascending=False).iloc[0]

st.success(
    f"Highest spending category: **{highest['ground_truth_category']}** "
    f"(₹{highest['amount']:,.0f})"
)


