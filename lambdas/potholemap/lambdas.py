"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import json
import logging
import pytz

from uuid import uuid4, UUID
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

from potholemap import httpstatus
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

        return handler


class QueryLambda(Lambda):
    @staticmethod
    def _extract_bounds(query_params: CaseInsensitiveDict) -> Optional[Tuple[float, float, float, float]]:
        nelat = query_params.get('nelat', None)
        nelng = query_params.get('nelng', None)
        swlat = query_params.get('swlat', None)
        swlng = query_params.get('swlng', None)

        if None in (nelat, nelng, swlat, swlng):
            return None

        try:
            return float(nelat), float(nelng), float(swlat), float(swlng)
        except ValueError:
            return None

    def handle(self, event: Event, context: Context) -> Response:
        bounds = QueryLambda._extract_bounds(event.query_params)
        if bounds is None:
            return JsonResponse(
                status_code=httpstatus.HTTP_400_BAD_REQUEST,
                data={'message': 'Query parameters (nelat, nelng, swlat, swlng) must be set correctly'},
            )

        # TODO: Implement DynamoDB query.
        generator = Random(0)
        potholes = [{
            "id": UUID(int=i),
            "deviceName": f'Test Device {i}',
            "timestamp": datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(seconds=i * 10),
            "confidence": generator.random(),
            "coordinates": [
                -31.958279460482014 + generator.random() * 0.5 - 0.25,
                115.84404945373534 + generator.random() * 0.5 - 0.25,
            ],
            "photoUrl": f'https://picsum.photos/seed/05/1920/1080?random={i}'
        } for i in range(100)]

        return JsonResponse(list(filter(
            lambda p: (bounds[2] < p['coordinates'][0] < bounds[0]
                       and bounds[3] < p['coordinates'][1] < bounds[1]), potholes)))


query_handler = QueryLambda().bind()
