import itertools
import string
from datetime import date
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from rates.database import db, ports, prices, regions
from rates.main import app
from rates.utils import PortDict, PriceDict, RegionDict


@pytest.fixture(scope="module", params=["asyncio"])
def anyio_backend(request):
    return request.param


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client, LifespanManager(
        app
    ):
        yield client


@pytest.fixture(scope="module")
async def region_list() -> list[RegionDict]:
    values: list[RegionDict] = [
        {
            "slug": "europe_south",
            "name": "Southern Europe",
            "parent_slug": None,
        },
        {
            "slug": "europe_south_west",
            "name": "Western Southern Europe",
            "parent_slug": "europe_south",
        },
        {
            "slug": "europe_south_east",
            "name": "Eastern Southern Europe",
            "parent_slug": "europe_south",
        },
        {
            "slug": "europe_north",
            "name": "Northern Europe",
            "parent_slug": None,
        },
        {
            "slug": "europe_north_main",
            "name": "Main Northern Europe",
            "parent_slug": "europe_north",
        },
        {
            "slug": "europe_north_baltic",
            "name": "Baltic North Europe",
            "parent_slug": "europe_north_main",
        },
        {
            "slug": "europe_north_rare",
            "name": "Unknown North Europe",
            "parent_slug": "europe_north_baltic",
        },
    ]

    await db.execute_many(regions.insert(), values=values)

    return values


@pytest.fixture(scope="module")
async def port_list(region_list: list[RegionDict]) -> list[PortDict]:
    values: list[PortDict] = [
        {"code": "AAAAA", "name": "Port A", "parent_slug": "europe_south"},
        {"code": "BBBBB", "name": "Port B", "parent_slug": "europe_south"},
        {"code": "CCCCC", "name": "Port C", "parent_slug": "europe_south_west"},
        {"code": "DDDDD", "name": "Port D", "parent_slug": "europe_south_west"},
        {"code": "EEEEE", "name": "Port E", "parent_slug": "europe_south_east"},
        {"code": "FFFFF", "name": "Port F", "parent_slug": "europe_north"},
        {"code": "GGGGG", "name": "Port G", "parent_slug": "europe_north_main"},
        {"code": "HHHHH", "name": "Port H", "parent_slug": "europe_north_main"},
        {"code": "IIIII", "name": "Port I", "parent_slug": "europe_north_main"},
        {"code": "JJJJJ", "name": "Port J", "parent_slug": "europe_north_main"},
        {"code": "KKKKK", "name": "Port K", "parent_slug": "europe_north_baltic"},
        {"code": "LLLLL", "name": "Port L", "parent_slug": "europe_north_baltic"},
        {"code": "MMMMM", "name": "Port M", "parent_slug": "europe_north_rare"},
    ]

    await db.execute_many(ports.insert(), values=values)

    return values


@pytest.fixture(scope="module")
async def price_list(port_list: list[PortDict]) -> list[PriceDict]:
    port_code_chars = string.ascii_uppercase[:12]
    values: list[PriceDict] = []

    for orig, dest in itertools.permutations(port_code_chars, 2):
        for dt in range(1, 21):
            orig_code = orig * 5
            dest_code = dest * 5
            day = date(2022, 9, dt)
            location_diff = abs(ord(dest) - ord(orig))
            location_mul = 50 if ord(dest) > ord(orig) else 60
            price = 500 + location_diff * location_mul + (dt % 5) * 10
            values.append(
                {
                    "orig_code": orig_code,
                    "dest_code": dest_code,
                    "day": day,
                    "price": price,
                }
            )

    values.append(
        {
            "orig_code": "MMMMM",
            "dest_code": "BBBBB",
            "day": date(2022, 9, 1),
            "price": 1000,
        }
    )

    values.append(
        {
            "orig_code": "MMMMM",
            "dest_code": "DDDDD",
            "day": date(2022, 9, 1),
            "price": 1000,
        }
    )

    values.append(
        {
            "orig_code": "CCCCC",
            "dest_code": "MMMMM",
            "day": date(2022, 9, 1),
            "price": 1000,
        }
    )

    await db.execute_many(prices.insert(), values=values)

    return values
