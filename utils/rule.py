import re

MERCHANT_RULES = {
    "NETFLIX": "Entertainment",
    "SPOTIFY": "Entertainment",
    "BOOKMYSHOW": "Entertainment",
    "PVR": "Entertainment",
    "HOTSTAR": "Entertainment",

    "SWIGGY": "Food & Dining",
    "ZOMATO": "Food & Dining",
    "DOMINOS": "Food & Dining",
    "MCDONALDS": "Food & Dining",
    "STARBUCKS": "Food & Dining",

    "BIGBASKET": "Groceries",
    "BLINKIT": "Groceries",
    "ZEPTO": "Groceries",
    "DMART": "Groceries",
    "RELIANCE": "Groceries",

    "UBER": "Travel & Transport",
    "OLA": "Travel & Transport",
    "RAPIDO": "Travel & Transport",
    "IRCTC": "Travel & Transport",

    "AMAZON": "Shopping",
    "FLIPKART": "Shopping",
    "MYNTRA": "Shopping",
    "AJIO": "Shopping",
    "CROMA": "Shopping",

    "APOLLO": "Healthcare",
    "PHARMEASY": "Healthcare",
    "PRACTO": "Healthcare",

    "UDEMY": "Education",
    "COURSERA": "Education",
    "GEEKSFORGEEKS": "Education",
}

_LETTER_RUNS = re.compile(r"[A-Z]+")

# Merchant names up to this length must match a whole word. Longer names may
# appear inside a word (e.g. "AMAZONPAY"). This stops short names such as
# "OLA" from matching inside unrelated words like "COCA COLA".
_MAX_WHOLE_WORD_LEN = 4


def categorize_by_rule(description):
    """Return the category for a known merchant, or None if no rule matches."""
    if not isinstance(description, str) or not description.strip():
        return None

    words = _LETTER_RUNS.findall(description.upper())
    for merchant, category in MERCHANT_RULES.items():
        for word in words:
            if word == merchant:
                return category
            if len(merchant) > _MAX_WHOLE_WORD_LEN and merchant in word:
                return category
    return None
