import os

from databases import Database
from sqlalchemy import create_engine, MetaData

from rates.config import settings


engine = create_engine(settings.db_url)
metadata = MetaData()

db = Database(settings.db_url)
