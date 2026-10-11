import pytest

from utils.rule import MERCHANT_RULES, categorize_by_rule


@pytest.mark.parametrize("merchant, category", MERCHANT_RULES.items())
def test_every_merchant_in_rules_maps_to_its_category(merchant, category):
    assert categorize_by_rule(merchant) == category


@pytest.mark.parametrize(
    "description, expected",
    [
        ("UPI-SWIGGY-98765", "Food & Dining"),
        ("swiggy order", "Food & Dining"),
        ("  Netflix   subscription ", "Entertainment"),
        ("AMAZONPAY 4432", "Shopping"),
        ("UBER TRIP BANGALORE", "Travel & Transport"),
    ],
)
def test_matches_merchant_inside_messy_descriptions(description, expected):
    assert categorize_by_rule(description) == expected


def test_short_merchant_name_does_not_match_inside_other_words():
    # "OLA" must not fire on "COCA COLA"
    assert categorize_by_rule("COCA COLA BOTTLE") is None


def test_standalone_short_merchant_name_still_matches():
    assert categorize_by_rule("OLA CABS RIDE") == "Travel & Transport"


@pytest.mark.parametrize("description", ["QWERTY UNKNOWN SHOP", "ATM WITHDRAWAL"])
def test_unknown_descriptions_return_none(description):
    assert categorize_by_rule(description) is None


@pytest.mark.parametrize("bad_input", ["", "   ", None, 123, float("nan")])
def test_empty_or_non_string_input_returns_none(bad_input):
    assert categorize_by_rule(bad_input) is None
