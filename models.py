from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class LoanApplication(db.Model):
    __tablename__ = "loan_applications"

    id = db.Column(db.Integer, primary_key=True)

    # Personal info
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    ssn = db.Column(db.Text, nullable=False)

    # Address (normalized)
    address_line_1 = db.Column(db.Text, nullable=False)
    address_line_2 = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    zip_code = db.Column(db.Text, nullable=False)

    # Credit info
    open_credit_lines = db.Column(db.Integer, nullable=False)
    requested_amount_cents = db.Column(db.Integer, nullable=False)

    # Loan terms (nullable until approved/quoted)
    total_loan_amount_cents = db.Column(db.Integer, nullable=True)
    interest_rate_bps = db.Column(db.Integer, nullable=True)
    term_months = db.Column(db.Integer, nullable=True)
    monthly_payment_cents = db.Column(db.Integer, nullable=True)

    # Metadata
    status = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=False), server_default=func.now(), nullable=True
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "ssn": self.ssn,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "open_credit_lines": self.open_credit_lines,
            "requested_amount_cents": self.requested_amount_cents,
            "total_loan_amount_cents": self.total_loan_amount_cents,
            "interest_rate_bps": self.interest_rate_bps,
            "term_months": self.term_months,
            "monthly_payment_cents": self.monthly_payment_cents,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
