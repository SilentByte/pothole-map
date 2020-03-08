"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

from typing import (
    Type,
    List,
    Any,
)

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

    limit = fields.Integer(required=False)


class PotholeSchema(Schema):
    id = fields.UUID(required=False)
    device_name = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    confidence = fields.Float(required=True)
    coordinates = fields.Tuple((fields.Float(), fields.Float()), required=True)
    photo_url = fields.String(required=False)


def apply_schema(schema: Type[Schema], data: str):
    return schema().loads(data)


def dump_schema_list(schema: Type[Schema], data: Any) -> List[dict]:
    # noinspection PyTypeChecker
    return schema().dump(data, many=True)
