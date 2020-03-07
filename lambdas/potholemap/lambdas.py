"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import json
import logging
import pytz
import geohash2

from uuid import UUID
from random import Random
from datetime import datetime, timedelta

from abc import abstractmethod
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Union,
)

from potholemap import httpstatus, schemas
from potholemap.collections import CaseInsensitiveDict

log = logging.getLogger(__name__)


def _jsonify(data: Union[dict, list]) -> str:
    class ExtendedEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, UUID):
                return str(o)
            elif isinstance(o, datetime):
                return o.isoformat()
            else:
                return json.JSONEncoder.default(self, o)

    return json.dumps(
        data,
        indent=None,
        separators=(',', ':'),
        sort_keys=True,
        cls=ExtendedEncoder,
    )


class Event:
    method: str
    headers: CaseInsensitiveDict
    query_params: CaseInsensitiveDict
    body: Any
    is_base64: bool

    def __init__(
            self,
            method: str = '',
            headers: Optional[Dict[str, str]] = None,
            query_params: Optional[Dict[str, str]] = None,
            body: Any = None,
            is_base64: bool = False
    ):
        self.method = method
        self.headers = CaseInsensitiveDict(headers)
        self.query_params = CaseInsensitiveDict(query_params)
        self.body = body
        self.is_base64 = is_base64


class Context:
    pass


class GatewayException(Exception):
    status_code = httpstatus.HTTP_500_INTERNAL_SERVER_ERROR


class BadRequestException(GatewayException):
    status_code = httpstatus.HTTP_400_BAD_REQUEST


class Response:
    status_code: int = httpstatus.HTTP_200_OK
    headers: Dict[str, str] = None
    body: Optional[str] = None

    def __init__(
            self,
            status_code: int = httpstatus.HTTP_200_OK,
            headers: Optional[Dict[str, str]] = None,
            body: Optional[str] = None,
    ):
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.body = body


class JsonResponse(Response):
    def __init__(
            self,
            data: Union[dict, list],
            status_code=httpstatus.HTTP_200_OK,
            headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code, headers, _jsonify(data))

        if 'Content-Type' not in self.headers:
            self.headers['Content-Type'] = 'application/json'


class Lambda:
    @abstractmethod
    def handle(self, event: Event, context: Context) -> Response:
        raise NotImplementedError()

    @staticmethod
    def translate_event(lambda_event: dict) -> Event:
        """
        Translates an event from an AWS service to a simplified internal structure.
        For available fields, see: <https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html>.
        """

        method = lambda_event.get('httpMethod', '').upper()
        headers = lambda_event.get('headers', {})
        query_params = lambda_event.get('queryStringParameters', {})
        body = lambda_event.get('body', '')
        is_base64 = lambda_event.get('isBase64Encoded', False)

        return Event(method, headers, query_params, body, is_base64)

    @staticmethod
    def translate_context(_lambda_context: dict) -> Context:
        return Context()

    def bind(self) -> callable:
        # noinspection PyBroadException
        def handler(event, context) -> dict:
            try:
                response = self.handle(
                    event=Lambda.translate_event(event),
                    context=Lambda.translate_context(context),
                )

                return {
                    'statusCode': response.status_code,
                    'headers': response.headers,
                    'body': response.body,
                }

            except GatewayException as e:
                log.warning(f'[GatewayException] {e}')
                return {
                    'statusCode': e.status_code,
                    'body': None,
                }

            except:
                log.exception('Unhandled exception')
                return {
                    'statusCode': httpstatus.HTTP_500_INTERNAL_SERVER_ERROR,
                    'body': None,
                }

        return handler


class QueryLambda(Lambda):
    @staticmethod
    def _parse_body(event: Event) -> Optional[dict]:
        try:
            return schemas.apply_schema(schemas.QuerySchema, event.body)
        except schemas.ValidationError:
            return None

    def handle(self, event: Event, context: Context) -> Response:
        data = QueryLambda._parse_body(event)
        if data is None:
            return JsonResponse(
                status_code=httpstatus.HTTP_400_BAD_REQUEST,
                data={'message': 'Invalid payload'},
            )

        nelat, nelng, swlat, swlng = data['bounds']
        limit = min(data['limit'], 100)

        # TODO: Implement as DynamoDB query.
        generator = Random(0)
        potholes = []
        for i in range(10000):
            coordinates = [
                -31.958279460482014 + (generator.random() * 2 - 1),
                115.84404945373534 + (generator.random() * 2 - 1),
            ]

            record = {
                "id": UUID(int=generator.getrandbits(128)),
                "deviceName": f'Test Device {i}',
                "timestamp": datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(seconds=i * 10),
                "confidence": generator.random(),
                "coordinates": coordinates,
                "geohash": geohash2.encode(coordinates[0], coordinates[1]),
                "photoUrl": f'https://picsum.photos/seed/05/1920/1080?random={i}'
            }

            potholes.append(record)

        lower = geohash2.encode(swlat, swlng)
        upper = geohash2.encode(nelat, nelng)

        potholes = list(filter(lambda p: lower <= p['geohash'] <= upper, potholes))
        potholes = sorted(potholes, key=lambda p: p['id'])
        potholes = potholes[:limit + 1]

        return JsonResponse({
            'potholes': potholes,
            'truncated': len(potholes) > limit,
        }, headers={
            'Access-Control-Allow-Origin': '*',
        })


query_handler = QueryLambda().bind()
