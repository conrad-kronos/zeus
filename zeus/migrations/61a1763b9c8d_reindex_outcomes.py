"""reindex_outcomes

Revision ID: 61a1763b9c8d
Revises: 340d5cc7e806
Create Date: 2019-08-09 12:47:22.165013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "61a1763b9c8d"
down_revision = "340d5cc7e806"
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("idx_build_outcomes", table_name="build")
    op.create_index(
        "idx_build_outcomes",
        "build",
        ["repository_id", "status", "result", "date_created"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("idx_build_outcomes", table_name="build")
    op.create_index(
        "idx_build_outcomes",
        "build",
        ["status", "result", "date_created"],
        unique=False,
    )
    # ### end Alembic commands ###
