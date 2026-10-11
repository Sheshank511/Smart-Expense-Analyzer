from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from utils.categorize import categorize


class FakeModel:
    """Stand-in for the trained classifier that records what it was asked."""

    def __init__(self, label):
        self.label = label
        self.calls = []

    def predict(self, texts):
        self.calls.append(list(texts))
        return [self.label] * len(texts)


def test_rule_wins_over_model_for_known_merchant():
    model = FakeModel("Shopping")
    assert categorize("swiggy order", model=model) == "Food & Dining"
    assert model.calls == []  # the model was never consulted


def test_model_is_used_when_no_rule_matches():
    model = FakeModel("Healthcare")
    assert categorize("some local clinic", model=model) == "Healthcare"
    assert model.calls == [["SOME LOCAL CLINIC"]]


def test_fallback_label_when_no_rule_and_no_model():
    assert categorize("some local clinic") == "Uncategorized"
    assert categorize("some local clinic", fallback="Other") == "Other"


def test_blank_description_returns_fallback_without_calling_model():
    model = FakeModel("Shopping")
    assert categorize("   ", model=model) == "Uncategorized"
    assert categorize(None, model=model) == "Uncategorized"
    assert model.calls == []


def test_works_with_a_real_sklearn_pipeline():
    texts = ["CITY CLINIC VISIT", "HEALTH CLINIC FEES", "BOOK STORE PURCHASE", "NOVEL BOOK STORE"]
    labels = ["Healthcare", "Healthcare", "Shopping", "Shopping"]
    pipe = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression(max_iter=1000))])
    pipe.fit(texts, labels)

    assert categorize("new clinic visit", model=pipe) == "Healthcare"
