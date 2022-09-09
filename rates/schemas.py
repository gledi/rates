from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class RatesQueryParams(BaseModel):
    origin: str
    destination: str
    date_from: date
    date_to: date


class DayAveragePrice(BaseModel):
    day: date
    average_price: Decimal | None
