from databases import Database
from sqlalchemy import (
    Column,
    Date,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
    create_engine,
)

from rates.config import settings
from rates.utils import Environment

engine = create_engine(settings.db_url)
metadata = MetaData()

regions = Table(
    "regions",
    metadata,
    Column("slug", Text, nullable=False),
    Column("name", Text, nullable=False),
    Column("parent_slug", Text, nullable=True),
    PrimaryKeyConstraint("slug", name="regions_pkey"),
    ForeignKeyConstraint(
        ["parent_slug"],
        ["regions.slug"],
        name="regions_parent_slug_fkey",
    ),
)

ports = Table(
    "ports",
    metadata,
    Column("code", Text, nullable=False),
    Column("name", Text, nullable=False),
    Column("parent_slug", Text, nullable=False),
    PrimaryKeyConstraint("code", name="ports_pkey"),
    ForeignKeyConstraint(
        ["parent_slug"],
        ["regions.slug"],
        name="ports_parent_slug_fkey",
    ),
)

prices = Table(
    "prices",
    metadata,
    Column("orig_code", Text, nullable=False),
    Column("dest_code", Text, nullable=False),
    Column("day", Date, nullable=False),
    Column("price", Integer, nullable=False),
    ForeignKeyConstraint(["orig_code"], ["ports.code"], name="prices_orig_code_fkey"),
    ForeignKeyConstraint(["dest_code"], ["ports.code"], name="prices_dest_code_fkey"),
)


_force_rollback = settings.environment == Environment.testing
db = Database(settings.db_url, force_rollback=_force_rollback)
