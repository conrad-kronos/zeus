"""repo_provider

Revision ID: 89a25650d379
Revises: f7c8c10f5aea
Create Date: 2017-07-14 14:44:49.308988

"""
import zeus
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "89a25650d379"
down_revision = "f7c8c10f5aea"
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "repository", sa.Column("external_id", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "repository",
        sa.Column("provider", zeus.db.types.enum.StrEnum(), nullable=False),
    )
    op.create_unique_constraint(
        "unq_external_id", "repository", ["provider", "external_id"]
    )


# ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("unq_external_id", "repository", type_="unique")
    op.drop_column("repository", "provider")
    op.drop_column("repository", "external_id")


# ### end Alembic commands ###
