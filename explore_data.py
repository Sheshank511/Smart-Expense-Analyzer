import pandas as pd

# Load dataset
df = pd.read_csv("transactions.csv")

# Display first 5 rows
print("First 5 Transactions")
print(df.head())

print("\n")

# Dataset information
print(df.info())

print("\n")

# Missing values
print("Missing Values")
print(df.isnull().sum())

print("\n")

# Category distribution
print("Category Distribution")
print(df["ground_truth_category"].value_counts())

print("\n")

# Amount statistics
print("Transaction Amount Statistics")
print(df["amount"].describe())