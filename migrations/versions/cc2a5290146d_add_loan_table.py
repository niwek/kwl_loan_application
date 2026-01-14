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
            id SERIAL PRIMARY KEY,

            -- Personal info
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            ssn TEXT NOT NULL,

            -- Address (normalized)
            address_line_1 TEXT NOT NULL,
            address_line_2 TEXT,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL,

            -- Credit info
            open_credit_lines INTEGER NOT NULL
                CHECK (open_credit_lines >= 0),

            requested_amount_cents INTEGER NOT NULL
                CHECK (requested_amount_cents > 0),

            -- Loan terms (nullable until approved)
            total_loan_amount_cents INTEGER
                CHECK (total_loan_amount_cents IS NULL OR total_loan_amount_cents > 0),

            interest_rate_bps INTEGER
                CHECK (interest_rate_bps IS NULL OR interest_rate_bps >= 0),

            term_months INTEGER
                CHECK (term_months IS NULL OR term_months > 0),

            monthly_payment_cents INTEGER
                CHECK (monthly_payment_cents IS NULL OR monthly_payment_cents >= 0),

            -- Metadata
            status TEXT NOT NULL
                CHECK (status IN ('pending', 'approved', 'rejected')),

            created_at TIMESTAMP DEFAULT now()
        );
        """
    )


def downgrade():
    op.execute("DROP TABLE loan_applications;")
