"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

from typing import Type
from marshmallow import (
    Schema,
    ValidationError,
    fields,
)

ValidationError = ValidationError


class QuerySchema(Schema):
    bounds = fields.Tuple((
        fields.Float(),
        fields.Float(),
        fields.Float(),
        fields.Float(),
    ), required=True)

    limit = fields.Integer(required=False, missing=10)


def apply_schema(schema: Type[Schema], data: str):
    return schema().loads(data)
