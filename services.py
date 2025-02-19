# service.py
from typing import List
import json
from decimal import Decimal
import uuid
from dataclasses import dataclass
from models import BookingRequest, Price


@dataclass
class HotelRate:
    """Represents the rate information from the hotel supplier"""

    hotel_code: str
    net_price: Decimal
    currency: str


class PricingService:
    def calculate_price(self, rate: HotelRate, target_currency: str) -> Price:
        """Calculate final price with markup and currency conversion"""
        price = Price(
            currency=rate.currency, net=rate.net_price, selling_currency=target_currency
        )
        price.calculate_selling_price()
        return price


class SupplierService:
    """Simulates calling an external hotel supplier API"""

    def get_hotel_rates(self, request: BookingRequest) -> List[HotelRate]:

        # Simluate rates, in reality hit some API.
        sample_rates = [
            HotelRate(
                hotel_code=str(uuid.uuid4())[:8],
                net_price=Decimal(str(100 + (i * 25.5))),
                currency=request.currency,
            )
            for i in range(min(request.options_quota, 5))
        ]
        return sample_rates


class BookingService:
    def __init__(self):
        self.supplier_service = SupplierService()
        self.pricing_service = PricingService()

    def process_request(self, request: BookingRequest) -> List[dict]:
        hotel_rates = self.supplier_service.get_hotel_rates(request)
        results = []
        for i, rate in enumerate(hotel_rates, 1):
            price = self.pricing_service.calculate_price(rate, request.currency)

            result = {
                "id": f"A#{i}",
                "hotelCodeSupplier": rate.hotel_code,
                "market": request.nationality,
                "price": {
                    "minimumSellingPrice": None,
                    "currency": price.currency,
                    "net": float(price.net),
                    "selling_price": float(price.selling_price),
                    "selling_currency": price.selling_currency,
                    "markup": float(price.markup),
                    "exchange_rate": float(price.exchange_rate),
                },
            }
            results.append(result)

        return results
