"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.path.exists(os.path.join(BASE_DIR, '.env.development')):
    load_dotenv(os.path.join(BASE_DIR, '.env.development'))
else:
    load_dotenv(os.path.join(BASE_DIR, '.env.production'))


def truthy(value):
    value = str(value)
    return len(value) != 0 and value.lower() not in ('false', 'no')


def optional(name, default_value):
    return os.getenv(name, default_value)


def required(name):
    return os.environ[name]


DEBUG = truthy(required('DEBUG'))
PRODUCTION = truthy(required('PRODUCTION'))

QUERY_DEFAULT_RESULT_COUNT = int(required('QUERY_DEFAULT_RESULT_COUNT'))
QUERY_MAX_RESULT_COUNT = int(required('QUERY_MAX_RESULT_COUNT'))

PHOTO_BUCKET_NAME = required('PHOTO_BUCKET_NAME')
PHOTO_KEY_PREFIX = optional('PHOTO_KEY_PREFIX', 'potholes/')

if DEBUG and PRODUCTION:
    raise ValueError('DEBUG and PRODUCTION cannot be true simultaneously')

DB_NAME = required('DB_NAME')
DB_USER = required('DB_USER')
DB_PASSWORD = required('DB_PASSWORD')
DB_HOST = required('DB_HOST')
DB_PORT = required('DB_PORT')
