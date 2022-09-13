from datetime import date
from enum import Enum
from typing import TypedDict


class Environment(str, Enum):
    testing = "testing"
    development = "development"
    production = "production"


class RegionDict(TypedDict):
    slug: str
    name: str
    parent_slug: str | None


class PortDict(TypedDict):
    code: str
    name: str
    parent_slug: str


class PriceDict(TypedDict):
    orig_code: str
    dest_code: str
    day: date
    price: int
