from databases import Database
from sqlalchemy import create_engine, MetaData

from rates.config import settings
from rates.utils import Environment


engine = create_engine(settings.db_url)
metadata = MetaData()

_force_rollback = settings.environment == Environment.testing
db = Database(settings.db_url, force_rollback=_force_rollback)
