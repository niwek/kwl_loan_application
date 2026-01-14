import random

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from urllib import parse

from marshmallow import ValidationError

from models import LoanApplication
from schemas import LoanApplicationRequestSchema

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{os.environ['DB_USER']}:{parse.quote_plus(os.environ['DB_PASS'])}@{os.environ['DB_SERVER']}:{os.environ['DB_PORT']}/{os.environ['DB']}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/ping")
def ping():
    return "Pong"


@app.route("/v1/loan_applications", methods=["POST"])
def create_loan_application():
    try:
        # Validation
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Expected JSON body"}), 400

        data = LoanApplicationRequestSchema().load(payload)

        data["open_credit_lines"] = random.randint(0, 100)
        loan = LoanApplication(**data)

        compute_loan_offer(loan)

        db.session.add(loan)
        db.session.commit()

        return jsonify({"message": "ok", "data": loan.to_dict()}), 201
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "message": err.messages}), 400
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": str(err)}), 500
    except Exception as err:
        return jsonify({"error": "Internal server error", "message": str(err)}), 500


def compute_loan_offer(loan: LoanApplication):
    if (
        loan.requested_amount_cents < 1000000
        or loan.requested_amount_cents > 5000000
        or loan.open_credit_lines > 50
    ):
        loan.status = "rejected"
        return
    elif loan.open_credit_lines < 10:
        loan.term_months = 36
        loan.interest_rate_bps = 1000
    elif 10 <= loan.open_credit_lines <= 50:
        loan.term_months = 24
        loan.interest_rate_bps = 2000
    loan.total_loan_amount_cents = loan.requested_amount_cents
    loan.monthly_payment_cents = calculate_monthly_payment_cents(
        loan.total_loan_amount_cents, loan.interest_rate_bps, loan.term_months
    )
    loan.status = "approved"


def calculate_monthly_payment_cents(
    total_loan_amount_cents: int, interest_rate_bps: int, term_months: int
):
    P = total_loan_amount_cents / 100.0  # convert to dollars
    r = (interest_rate_bps / 10_000) / 12.0
    n = term_months

    if r == 0:  # zero-interest loan
        payment = P / n
    else:
        payment = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    return round(payment * 100)  # back to cents


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)
