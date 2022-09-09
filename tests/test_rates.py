from typing import AsyncGenerator
from pprint import pp
from datetime import date

import pytest
from fastapi import status
from httpx import AsyncClient

from rates.main import app


@pytest.fixture(params=['asyncio'])
def anyio_backend(request):
    return request.param


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


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
    response = await client.get("rates", params={
        "origin": "QWERTY",
        "destination": "ASDFG",
        "date_from": date(2022, 9, 1),
        "date_to": date(2022, 8, 28),
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': [{'loc': ['date_to'], 'msg': "'date_from' must be after 'date_to'", 'type': 'value_error'}]}
