"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import json
import logging

from abc import abstractmethod
from typing import (
    Optional,
    Union,
    Dict,
    Any,
)

from potholemap import httpstatus
from potholemap.collections import CaseInsensitiveDict

log = logging.getLogger(__name__)


def _jsonify(data: Union[dict, list]) -> str:
    return json.dumps(data, indent=None, separators=(',', ':'), sort_keys=True)


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
    def handle(self, event: Event, context: Context) -> Response:
        return JsonResponse({
            'test': 'ok',
        })


query_handler = QueryLambda().bind()
