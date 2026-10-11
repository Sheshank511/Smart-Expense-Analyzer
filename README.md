# Smart Expense Analyzer

An end-to-end machine learning project for analyzing personal expenses.

## Features

- Expense Categorization using NLP
- Hybrid Rule + ML Prediction
- Fraud Detection using Isolation Forest
- Financial Analytics Dashboard
- Transaction Explorer
- Streamlit Web Application

## Tech Stack

- Python
- Scikit-learn
- Pandas
- Plotly
- Streamlit
- Joblib

## ML Models

- TF-IDF
- Logistic Regression
- Isolation Forest

## Dashboard

- Dashboard
- Analytics
- Expense Predictor
- Fraud Detection
- Transaction Explorer

![CI](https://github.com/https://github.com/Sheshank511/https://github.com/Sheshank511/Smart-Expense-Analyzer/actions/workflows/ci.yml/badge.svg)

## Architecture

```
transactions.csv
      |
      v
utils/preprocess.py  --> normalize text, parse dates/amounts, drop bad rows
      |
      v
utils/categorize.py  --> hybrid categorization
      |                    1. utils/rule.py: merchant rules (known merchants)
      |                    2. TF-IDF + Logistic Regression (models/expense_classifier.pkl)
      v
Isolation Forest     --> flags unusual transactions
      |
      v
Streamlit app (app.py + pages/) --> dashboard, analytics, predictor, fraud detection, explorer
```

## Setup

```bash
git clone https://github.com/https://github.com/Sheshank511/https://github.com/Sheshank511/Smart-Expense-Analyzer.git
cd https://github.com/Sheshank511/https://github.com/Sheshank511/Smart-Expense-Analyzer
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
streamlit run app.py
```

## Testing

```bash
pytest -v
pytest --cov=utils --cov-report=term-missing
```

Tests live in `tests/` and cover text preprocessing, merchant rule matching, and
the hybrid rule-then-model categorization. GitHub Actions runs them on every
push and pull request, on Python 3.10, 3.11 and 3.12 (`.github/workflows/ci.yml`).

# Smart-Expense-Analyzer
An end-to-end Machine Learning and Data Analytics application that automatically categorizes financial transactions, detects suspicious spending patterns, and provides interactive insights through a Stream-lit dashboard.
