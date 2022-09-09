from datetime import date
from decimal import Decimal

from pydantic import BaseModel, validator


class RatesQueryParams(BaseModel):
    origin: str
    destination: str
    date_from: date
    date_to: date

    @validator("date_to")
    def date_to_must_be_after_date_from(cls, val, values, **kwargs):
        if val < values.get("date_from", date.max):
            raise ValueError("'date_from' must be after 'date_to'")
        return val


class DayAveragePrice(BaseModel):
    day: date
    average_price: Decimal | None
