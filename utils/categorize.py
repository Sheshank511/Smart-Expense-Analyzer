from utils.preprocess import clean_description
from utils.rule import categorize_by_rule


def categorize(description, model=None, fallback="Uncategorized"):
    """Hybrid categorization: merchant rules first, ML model as fallback.

    `model` is any object with a scikit-learn style `predict(list_of_text)`.
    """
    cleaned = clean_description(description)
    if not cleaned:
        return fallback

    rule_category = categorize_by_rule(cleaned)
    if rule_category is not None:
        return rule_category

    if model is not None:
        return str(model.predict([cleaned])[0])

    return fallback
