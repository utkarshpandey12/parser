from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from constants import (
    DEFAULT_CURRENCY,
    DEFAULT_LANGUAGE,
    DEFAULT_NATIONALITY,
    EXCHANGE_RATES,
    MAX_OPTIONS_QUOTA,
    VALID_CURRENCIES,
    VALID_LANGUAGES,
    VALID_NATIONALITIES,
)
from exceptions import (
    InvalidDateError,
    InvalidParametersError,
    InvalidPaxConfigurationError,
)


@dataclass
class Parameter:
    password: str
    username: str
    company_id: int

    @classmethod
    def from_xml(cls, param_elem) -> "Parameter":
        if not all(
            attr in param_elem.attrib for attr in ["password", "username", "CompanyID"]
        ):
            raise InvalidParametersError("Missing required parameters")

        return cls(
            password=param_elem.attrib["password"],
            username=param_elem.attrib["username"],
            company_id=int(param_elem.attrib["CompanyID"]),
        )


@dataclass
class Passenger:
    age: int
    type: str = None

    def __post_init__(self):
        self.type = "Child" if self.age <= 5 else "Adult"


@dataclass
class Room:
    passengers: List[Passenger]
    allowed_guest_count: int
    allowed_child_count: int

    def validate(self):
        if len(self.passengers) > self.allowed_guest_count:
            raise InvalidPaxConfigurationError(
                f"Room exceeds maximum guest count of {self.allowed_guest_count}"
            )

        children = [p for p in self.passengers if p.type == "Child"]
        adults = [p for p in self.passengers if p.type == "Adult"]

        if len(children) > self.allowed_child_count:
            raise InvalidPaxConfigurationError(
                f"Room exceeds maximum child count of {self.allowed_child_count}"
            )

        if len(children) > 0 and len(adults) == 0:
            raise InvalidPaxConfigurationError(
                "Children must have at least one adult in the room"
            )


@dataclass
class Price:
    currency: str
    net: Decimal
    selling_currency: str
    markup: Decimal = Decimal("0.032")
    minimum_selling_price: Optional[Decimal] = None
    selling_price: Optional[Decimal] = None
    exchange_rate: Decimal = Decimal("1.0")

    def calculate_selling_price(self):
        self.selling_price = self.net * (1 + self.markup)

        if self.currency != self.selling_currency:
            self.exchange_rate = Decimal(
                str(EXCHANGE_RATES[self.currency][self.selling_currency])
            )
            self.selling_price *= self.exchange_rate

        self.selling_price = self.selling_price.quantize(Decimal("0.01"))


@dataclass
class BookingRequest:
    language_code: str
    options_quota: int
    parameters: Parameter
    search_type: str
    start_date: datetime
    end_date: datetime
    currency: str
    nationality: str
    rooms: List[Room]

    def __post_init__(self):
        self.validate()

    def validate(self):
        # Validate language
        if self.language_code not in VALID_LANGUAGES:
            self.language_code = DEFAULT_LANGUAGE

        # Validate options quota __define_ocg__
        if self.options_quota > MAX_OPTIONS_QUOTA:
            raise InvalidParametersError(
                f"Options quota cannot exceed {MAX_OPTIONS_QUOTA}"
            )

        # Validate dates
        today = datetime.now()
        if (self.start_date - today).days < 2:
            raise InvalidDateError("Start date must be at least 2 days from today")

        stay_duration = (self.end_date - self.start_date).days
        if stay_duration < 3:
            raise InvalidDateError("Stay duration must be at least 3 nights")

        # Validate currency and nationality
        if self.currency not in VALID_CURRENCIES:
            self.currency = DEFAULT_CURRENCY
        if self.nationality not in VALID_NATIONALITIES:
            self.nationality = DEFAULT_NATIONALITY
