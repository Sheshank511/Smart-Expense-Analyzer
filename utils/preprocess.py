import pandas as pd


def clean_description(text):
    """Normalize a transaction description: trim, collapse spaces, uppercase."""
    if text is None or pd.isna(text):
        return ""
    return " ".join(str(text).split()).upper()


def preprocess_transactions(df, drop_duplicates=True):
    """Return a cleaned copy of a transactions DataFrame.

    - rows with a missing or blank description are dropped
    - descriptions are normalized with clean_description
    - if a "date" column exists, it is parsed and unparseable rows are dropped
    - if an "amount" column exists, it is made numeric and bad rows are dropped
    - exact duplicate rows are dropped unless drop_duplicates=False
    The input DataFrame is never modified.
    """
    out = df.copy()

    out = out.dropna(subset=["description"])
    out["description"] = out["description"].map(clean_description)
    out = out[out["description"] != ""]

    if "date" in out.columns:
        out["date"] = pd.to_datetime(out["date"], errors="coerce")
        out = out.dropna(subset=["date"])

    if "amount" in out.columns:
        out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
        out = out.dropna(subset=["amount"])

    if drop_duplicates:
        out = out.drop_duplicates()

    return out.reset_index(drop=True)
