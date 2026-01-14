import random

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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


@app.route("/v1/loan_application", methods=["POST"])
def create_loan_application():
    try:
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Expected JSON body"}), 400

        data = LoanApplicationRequestSchema().load(payload)

        # At this point `data` is validated.
        # TODO: insert into DB

        data["open_credit_lines"] = random.randint(0, 100)
        data["status"] = "pending"

        loan = LoanApplication(**data)

        db.session.add(loan)
        db.session.commit()

        return jsonify({"message": "ok", "data": data}), 201
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "fields": err.messages}), 400
    except Exception as err:
        return jsonify({"error": "Internal server error", "fields": str(err)}), 500


if __name__ == "__main__":
    app.run(debug=True)
