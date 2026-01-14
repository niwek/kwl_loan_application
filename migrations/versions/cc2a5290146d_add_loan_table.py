"""add loan table

Revision ID: cc2a5290146d
Revises: 
Create Date: 2026-01-14 00:12:45.671456

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cc2a5290146d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
               CREATE TABLE loan_applications
               (
                   id         SERIAL PRIMARY KEY,
                   amount     NUMERIC(10, 2) NOT NULL,
                   status     TEXT           NOT NULL,
                   created_at TIMESTAMP DEFAULT now()
               );
               """
    )


def downgrade():
    op.execute("DROP TABLE loan_applications;")
