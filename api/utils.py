import json
import datetime

from flask import abort, Response
from marshmallow import Schema, fields, validates
from marshmallow.validate import Length, Range

class EmailPasswordSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=8, max=80))


class RegisterUserSchema(EmailPasswordSchema):
    username = fields.Str(required=True, validate=Length(min=3, max=80))

class CreateProjectSchema(EmailPasswordSchema):
    name = fields.Str(required=True, validate=Length(min=3, max=80))
    description = fields.Str(required=True, validate=Length(min=10, max=256))
    contract_value = fields.Float(
        required=True, validate=Range(min=1, max=1000000))
    percentage_return = fields.Float(
        required=True, validate=Range(min=1, max=100))
    end_date = fields.Date(required=True)

    @validates('end_date')
    def is_not_in_past(self, value):
        if value <= datetime.date.today():
            raise ValidationError("The end date must be in the future.")


def json_abort(message, status):
    abort(Response(json.dumps(message), status))
