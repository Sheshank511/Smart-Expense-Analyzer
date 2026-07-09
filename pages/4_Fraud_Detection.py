import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fraud Detection",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Fraud Detection Dashboard")

# -----------------------------
# Load Fraud Report
# -----------------------------
try:
    fraud = pd.read_csv("data/fraud_report.csv")
except FileNotFoundError:
    st.error("fraud_report.csv not found. Please run anomaly_detection.py first.")
    st.stop()

# -----------------------------
# Convert Date
# -----------------------------
if "date" in fraud.columns:
    fraud["date"] = pd.to_datetime(fraud["date"])

# -----------------------------
# Risk Column (if missing)
# -----------------------------
if "Risk" not in fraud.columns:

    def risk(amount):
        amount = abs(amount)

        if amount > 50000:
            return "HIGH"
        elif amount > 25000:
            return "MEDIUM"
        else:
            return "LOW"

    fraud["Risk"] = fraud["amount"].apply(risk)

# -----------------------------
# KPI Cards
# -----------------------------
total_alerts = len(fraud)
high = len(fraud[fraud["Risk"] == "HIGH"])
medium = len(fraud[fraud["Risk"] == "MEDIUM"])
low = len(fraud[fraud["Risk"] == "LOW"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("🚨 Total Alerts", total_alerts)
c2.metric("🔴 High Risk", high)
c3.metric("🟠 Medium Risk", medium)
c4.metric("🟢 Low Risk", low)

st.divider()

# -----------------------------
# Sidebar Filter
# -----------------------------
risk_filter = st.sidebar.selectbox(
    "Risk Level",
    ["All", "HIGH", "MEDIUM", "LOW"]
)

filtered = fraud.copy()

if risk_filter != "All":
    filtered = filtered[
        filtered["Risk"] == risk_filter
    ]

# -----------------------------
# Risk Distribution
# -----------------------------
left, right = st.columns(2)

risk_chart = (
    filtered["Risk"]
    .value_counts()
    .reset_index()
)

risk_chart.columns = ["Risk", "Count"]

fig1 = px.pie(
    risk_chart,
    values="Count",
    names="Risk",
    title="Risk Distribution"
)

left.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Top Fraud Merchants
# -----------------------------
merchant_chart = (
    filtered.groupby("merchant")["amount"]
    .sum()
    .abs()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    merchant_chart,
    x="merchant",
    y="amount",
    title="Top Suspicious Merchants"
)

right.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Search
# -----------------------------
st.subheader("🔍 Search Merchant")

search = st.text_input("Merchant Name")

if search:

    filtered = filtered[
        filtered["merchant"]
        .str.contains(search, case=False)
    ]

# -----------------------------
# Fraud Table
# -----------------------------
st.subheader("🚨 Suspicious Transactions")

st.dataframe(
    filtered,
    use_container_width=True
)

# -----------------------------
# Download Report
# -----------------------------
csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Fraud Report",
    csv,
    file_name="fraud_report.csv",
    mime="text/csv"
)

# -----------------------------
# Insights
# -----------------------------
st.subheader("💡 Fraud Insights")

if len(filtered):

    highest = filtered.iloc[
        filtered["amount"].abs().argmax()
    ]

    st.success(
        f"""
Highest suspicious transaction:

**Merchant:** {highest['merchant']}

**Amount:** ₹{abs(highest['amount']):,.2f}

**Risk:** {highest['Risk']}
"""
    )
else:
    st.info("No transactions match the selected filter.")