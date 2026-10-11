import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from utils.preprocess import preprocess_transactions

# Load dataset
df = preprocess_transactions(pd.read_csv("data/transactions.csv"), drop_duplicates=False)

# Features and labels
X = df["description"]
y = df["ground_truth_category"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Train model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
print("=" * 50)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("=" * 50)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "expense_classifier.pkl")

print("\nModel saved as expense_classifier.pkl")