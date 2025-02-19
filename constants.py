from typing import Set, Dict

VALID_LANGUAGES: Set[str] = {"en", "fr", "de", "es"}
VALID_CURRENCIES: Set[str] = {"EUR", "USD", "GBP"}
VALID_NATIONALITIES: Set[str] = {"US", "GB", "CA"}
VALID_MARKETS: Set[str] = {"US", "GB", "CA", "ES"}

DEFAULT_LANGUAGE = "en"
DEFAULT_CURRENCY = "EUR"
DEFAULT_NATIONALITY = "US"
DEFAULT_MARKET = "ES"
DEFAULT_OPTIONS_QUOTA = 20
MAX_OPTIONS_QUOTA = 50

EXCHANGE_RATES: Dict[str, Dict[str, float]] = {
    "EUR": {"USD": 1.1, "GBP": 0.86},
    "USD": {"EUR": 0.91, "GBP": 0.78},
    "GBP": {"EUR": 1.16, "USD": 1.28},
}
