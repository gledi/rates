#!/usr/bin/env python
import argparse
import logging
import sys
from datetime import date

import uvicorn
from fastapi import Depends, FastAPI, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from rates import queries
from rates.database import db
from rates.schemas import DayAveragePrice, RatesQueryParams

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
    date_to: date = Query(...),
) -> RatesQueryParams:
    try:
        return RatesQueryParams(
            origin=origin, destination=destination, date_from=date_from, date_to=date_to
        )
    except ValidationError as exc:
        logger.error("Invalid parameters", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(exc.errors()),
        )


@app.get("/")
def get_root() -> dict[str, str]:
    return {"message": "Xeneta Rates Task"}


@app.get("/rates", response_model=list[DayAveragePrice])
async def get_rates(
    params: RatesQueryParams = Depends(rates_params),
) -> list[DayAveragePrice]:
    rows = await db.fetch_all(queries.AVERAGE_PRICES, values=params.dict())
    result = [DayAveragePrice(**row._mapping) for row in rows]
    return result


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", "-a", default="0.0.0.0")
    parser.add_argument("--port", "-p", type=int, default=8000)
    parser.add_argument("--workers", "-w", type=int, default=1)

    return parser


def main(argv=None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    parser = get_parser()
    args = parser.parse_args(argv)

    uvicorn.run(app=app, host=args.host, port=args.port, workers=args.workers)


if __name__ == "__main__":
    sys.exit(main())
