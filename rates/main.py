from datetime import date
from fastapi import FastAPI, Depends, Query

from rates.database import db
from rates.schemas import RatesQueryParams, DayAveragePrice
from rates import queries


app = FastAPI(title="Xeneta Rates Task")


@app.on_event("startup")
async def on_startup() -> None:
    if not db.is_connected:
        await db.connect()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    if db.is_connected:
        await db.disconnect()


async def rates_params(
        origin: str = Query(default=...),
        destination: str = Query(default=...),
        date_from: date = Query(default=...),
        date_to: date = Query(default=...)) -> RatesQueryParams:
    return RatesQueryParams(origin=origin, destination=destination, date_from=date_from, date_to=date_to)



@app.get("/")
def get_root():
    return {"message": "Xeneta Rates Task"}


@app.get("/rates", response_model=list[DayAveragePrice])
async def get_rates(params: RatesQueryParams = Depends(rates_params)):
    rows = await db.fetch_all(queries.AVERAGE_PRICES, values=params.dict())
    result = [DayAveragePrice(**row._mapping) for row in rows]
    return result
