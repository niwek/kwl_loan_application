from marshmallow import Schema, fields, validate, ValidationError


class LoanApplicationRequestSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=validate.Length(min=7, max=30))

    # Store as string to preserve leading zeros; validate basic format
    ssn = fields.Str(required=True, validate=validate.Regexp(r"^\d{9}$"))

    address_line_1 = fields.Str(required=True)
    address_line_2 = fields.Str(required=False, allow_none=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True, validate=validate.Length(equal=2))  # "NY"
    zip_code = fields.Str(required=True, validate=validate.Regexp(r"^\d{5}(-\d{4})?$"))

    requested_amount_cents = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        metadata={"description": "Loan amount in cents"},
    )
