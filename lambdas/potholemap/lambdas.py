"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import json
import logging
import base64
import boto3

from uuid import UUID, uuid4
from datetime import datetime

from abc import abstractmethod
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

from potholemap import (
    httpstatus,
    schemas,
    settings,
)

from potholemap.db import Repo
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


def _generate_s3_photo_key(id: UUID) -> str:
    return settings.PHOTO_KEY_PREFIX + str(id)


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

        repo = Repo(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
        )

        s3 = boto3.client('s3')
        limit = min(data.get('limit', settings.QUERY_DEFAULT_RESULT_COUNT), settings.QUERY_MAX_RESULT_COUNT)
        potholes = repo.query_potholes_within_bounds(
            data['bounds'], limit + 1,
            lambda id: s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.PHOTO_BUCKET_NAME,
                    'Key': _generate_s3_photo_key(id),
                },
                ExpiresIn=60 * 60 * 24,
            )
        )

        return JsonResponse({
            'potholes': schemas.dump_schema_list(schemas.PotholeSchema, potholes),
            'truncated': len(potholes) > limit,
        }, headers={
            'Access-Control-Allow-Origin': settings.ACCESS_CONTROL_ALLOW_ORIGIN,
        })


def queue_handler(event, _context) -> None:
    record_id = uuid4()
    pothole_data = schemas.apply_schema(schemas.PotholeEventSchema, event)

    s3 = boto3.client('s3')
    s3.put_object(
        # TODO: Configure properly for existing setup.
        Bucket=settings.PHOTO_BUCKET_NAME,
        Key=_generate_s3_photo_key(record_id),
        Body=base64.b64decode(pothole_data['photo_data']),
    )

    repo = Repo(
        host=settings.DB_HOST,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
    )

    repo.insert_pothole(
        id=record_id,
        device_name=pothole_data['device_name'],
        timestamp=pothole_data['timestamp'],
        confidence=pothole_data['confidence'],
        coordinates=pothole_data['coordinates'],
    )


query_handler = QueryLambda().bind()
