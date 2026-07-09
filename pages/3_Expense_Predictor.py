import streamlit as st
import joblib
import pandas as pd

from utils.rule import MERCHANT_RULES

st.set_page_config(
    page_title="Expense Predictor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Expense Category Predictor")

model = joblib.load("models/expense_classifier.pkl")

text = st.text_input(
    "Enter Transaction Description",
    placeholder="Example: UPI-ZOMATO-123456@okhdfcbank"
)

if st.button("Predict"):

    description = text.upper()

    category = None

    method = None

    confidence = None

    # -------------------------
    # Rule Engine
    # -------------------------

    for merchant, cat in MERCHANT_RULES.items():

        if merchant in description:

            category = cat
            method = "Rule Based"
            confidence = 100

            break

    # -------------------------
    # Machine Learning
    # -------------------------

    if category is None:

        probs = model.predict_proba([text])[0]

        category = model.classes_[probs.argmax()]

        confidence = probs.max() * 100

        method = "Machine Learning"

    st.success(f"Category : {category}")

    st.info(f"Method : {method}")

    st.info(f"Confidence : {confidence:.2f}%")

    # -------------------------
    # Probability Table
    # -------------------------

    if method == "Machine Learning":

        st.subheader("Prediction Probabilities")

        probability_table = pd.DataFrame({

            "Category": model.classes_,

            "Probability (%)": (probs * 100).round(2)

        })

        st.dataframe(probability_table)