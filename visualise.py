import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("transactions.csv")

category_counts = df["ground_truth_category"].value_counts()

plt.figure(figsize=(10,5))
category_counts.plot(kind="bar")

plt.title("Transaction Categories")
plt.xlabel("Category")
plt.ylabel("Count")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
