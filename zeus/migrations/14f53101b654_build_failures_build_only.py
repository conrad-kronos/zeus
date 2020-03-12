"""build_failures_build_only

Revision ID: 14f53101b654
Revises: 16414a5b4ed9
Create Date: 2020-03-02 15:01:16.684848

"""
import zeus
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "14f53101b654"
down_revision = "16414a5b4ed9"
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "failurereason", sa.Column("build_id", zeus.db.types.guid.GUID(), nullable=True)
    )
    op.alter_column(
        "failurereason", "job_id", existing_type=postgresql.UUID(), nullable=True
    )
    op.drop_constraint("unq_failurereason_key", "failurereason", type_="unique")
    op.create_unique_constraint(
        "unq_failurereason_key", "failurereason", ["build_id", "job_id", "reason"]
    )
    op.create_foreign_key(
        None, "failurereason", "build", ["build_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "failurereason", type_="foreignkey")
    op.drop_constraint("unq_failurereason_key", "failurereason", type_="unique")
    op.create_unique_constraint(
        "unq_failurereason_key", "failurereason", ["job_id", "reason"]
    )
    op.alter_column(
        "failurereason", "job_id", existing_type=postgresql.UUID(), nullable=False
    )
    op.drop_column("failurereason", "build_id")
    # ### end Alembic commands ###