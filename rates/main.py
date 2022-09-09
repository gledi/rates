import logging

from datetime import date
from pydantic import ValidationError
from fastapi import FastAPI, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException

from rates.database import db
from rates.schemas import RatesQueryParams, DayAveragePrice
from rates import queries


logger = logging.getLogger(__name__)

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
        origin: str = Query(...),
        destination: str = Query(...),
        date_from: date = Query(...),
        date_to: date = Query(...)) -> RatesQueryParams:
    try:
        return RatesQueryParams(origin=origin, destination=destination, date_from=date_from, date_to=date_to)
    except ValidationError as exc:
        logger.error("Invalid parameters", exc_info=exc)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=jsonable_encoder(exc.errors()))


@app.get("/")
def get_root():
    return {"message": "Xeneta Rates Task"}


@app.get("/rates", response_model=list[DayAveragePrice])
async def get_rates(params: RatesQueryParams = Depends(rates_params)):
    rows = await db.fetch_all(queries.AVERAGE_PRICES, values=params.dict())
    result = [DayAveragePrice(**row._mapping) for row in rows]
    return result
