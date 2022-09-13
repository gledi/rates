from datetime import date
from typing import Any

import pytest
from fastapi import status
from httpx import AsyncClient

from rates.utils import PriceDict


@pytest.mark.anyio
async def test_get_root(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Xeneta Rates Task"}


@pytest.mark.anyio
async def test_rates_requires_all_parameters(client: AsyncClient) -> None:
    response = await client.get("/rates")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_rates_to_date_cannot_come_before_from_date(client: AsyncClient) -> None:
    response = await client.get(
        "rates",
        params={
            "origin": "QWERTY",
            "destination": "ASDFG",
            "date_from": date(2022, 9, 1),
            "date_to": date(2022, 8, 28),
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["date_to"],
                "msg": "'date_from' must be after 'date_to'",
                "type": "value_error",
            }
        ]
    }


@pytest.mark.anyio
async def test_average_price_for_less_than_three_rates_should_be_null(
    client: AsyncClient, price_list: list[dict[str, Any]]
) -> None:
    response = await client.get(
        "rates",
        params={
            "origin": "MMMM",
            "destination": "europe_south",
            "date_from": date(2022, 9, 1),
            "date_to": date(2022, 9, 2),
        },
    )

    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"day": "2022-09-01", "average_price": None},
        {"day": "2022-09-02", "average_price": None},
    ]


@pytest.mark.anyio
async def test_average_price_with_three_or_more_prices(
    client: AsyncClient, price_list: list[PriceDict]
) -> None:
    response = await client.get(
        "rates",
        params={
            "origin": "AAAAA",
            "destination": "europe_north_main",
            "date_from": date(2022, 9, 1),
            "date_to": date(2022, 9, 2),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"day": "2022-09-01", "average_price": 935.0},
        {"day": "2022-09-02", "average_price": 945.0},
    ]


@pytest.mark.anyio
async def test_period_with_no_prices_should_display_the_dates(
    client: AsyncClient, price_list: list[PriceDict]
) -> None:
    response = await client.get(
        "rates",
        params={
            "origin": "AAAAA",
            "destination": "europe_north_main",
            "date_from": date(2022, 5, 1),
            "date_to": date(2022, 5, 3),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"day": "2022-05-01", "average_price": None},
        {"day": "2022-05-02", "average_price": None},
        {"day": "2022-05-03", "average_price": None},
    ]
