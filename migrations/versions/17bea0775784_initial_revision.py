"""Initial revision

Revision ID: 17bea0775784
Revises:
Create Date: 2022-09-12 17:23:45.514735

"""
from alembic import op
import sqlalchemy as sa


revision = "17bea0775784"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "regions",
        sa.Column("slug", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("parent_slug", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_slug"], ["regions.slug"], name="regions_parent_slug_fkey"
        ),
        sa.PrimaryKeyConstraint("slug", name="regions_pkey"),
    )
    op.create_table(
        "ports",
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("parent_slug", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_slug"], ["regions.slug"], name="ports_parent_slug_fkey"
        ),
        sa.PrimaryKeyConstraint("code", name="ports_pkey"),
    )
    op.create_table(
        "prices",
        sa.Column("orig_code", sa.Text(), nullable=False),
        sa.Column("dest_code", sa.Text(), nullable=False),
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dest_code"], ["ports.code"], name="prices_dest_code_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["orig_code"], ["ports.code"], name="prices_orig_code_fkey"
        ),
    )


def downgrade() -> None:
    op.drop_table("prices")
    op.drop_table("ports")
    op.drop_table("regions")
