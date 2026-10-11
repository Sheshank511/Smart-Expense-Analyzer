import pandas as pd
import pytest

from utils.preprocess import clean_description, preprocess_transactions


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("  swiggy order  ", "SWIGGY ORDER"),
        ("Big   Bazaar", "BIG BAZAAR"),
        ("UPI-Amazon-123", "UPI-AMAZON-123"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_clean_description_normalizes_text(raw, expected):
    assert clean_description(raw) == expected


@pytest.mark.parametrize("missing", [None, float("nan"), pd.NA])
def test_clean_description_handles_missing_values(missing):
    assert clean_description(missing) == ""


@pytest.fixture
def raw_df():
    return pd.DataFrame(
        {
            "date": ["2026-01-05", "2026-01-05", "2026-01-07", "not-a-date", "2026-01-09"],
            "description": ["swiggy 123", "swiggy 123", "Uber Ride", "Zomato", None],
            "amount": [250.0, 250.0, None, 180.0, 90.0],
        }
    )


def test_drops_duplicates_missing_amounts_bad_dates_and_missing_descriptions(raw_df):
    out = preprocess_transactions(raw_df)
    # kept: only the first swiggy row. The duplicate, the missing amount,
    # the invalid date and the missing description are all removed.
    assert len(out) == 1
    assert out.loc[0, "description"] == "SWIGGY 123"


def test_output_has_clean_dtypes(raw_df):
    out = preprocess_transactions(raw_df)
    assert pd.api.types.is_datetime64_any_dtype(out["date"])
    assert pd.api.types.is_numeric_dtype(out["amount"])


def test_does_not_mutate_input(raw_df):
    snapshot = raw_df.copy(deep=True)
    preprocess_transactions(raw_df)
    pd.testing.assert_frame_equal(raw_df, snapshot)


def test_duplicates_can_be_kept():
    df = pd.DataFrame({"description": ["swiggy", "swiggy"]})
    assert len(preprocess_transactions(df, drop_duplicates=True)) == 1
    assert len(preprocess_transactions(df, drop_duplicates=False)) == 2


def test_works_without_optional_columns():
    df = pd.DataFrame({"description": ["swiggy", " zomato "], "ground_truth_category": ["a", "b"]})
    out = preprocess_transactions(df)
    assert list(out["description"]) == ["SWIGGY", "ZOMATO"]


def test_empty_dataframe_returns_empty():
    empty = pd.DataFrame(columns=["date", "description", "amount"])
    assert len(preprocess_transactions(empty)) == 0
