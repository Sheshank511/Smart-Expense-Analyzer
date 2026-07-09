import streamlit as st

st.set_page_config(
    page_title="Smart Expense Analyzer",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Smart Expense Analyzer")

st.markdown("""
Welcome to the **Smart Expense Analyzer**.

Use the sidebar to navigate between:
- 📊 Dashboard
- 📈 Analytics
- 🤖 Expense Predictor
- 🚨 Fraud Detection
- 🔍 Transaction Explorer
""")