"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import pytz
import psycopg2
import geohash2

from typing import (
    Tuple,
    List,
    Optional,
)

from uuid import uuid4
from datetime import datetime


def _utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=pytz.utc)


DatabaseError = psycopg2.Error


class Pothole:
    id: Optional[str]
    device_name: str
    timestamp: datetime
    confidence: float
    coordinates: Tuple[float, float]
    photo_url: Optional[str]

    def __init__(self, id: Optional[str], device_name: str, timestamp: datetime,
                 confidence: float, coordinates: Tuple[float, float], photo_url: Optional[str]):
        self.id = id
        self.device_name = device_name
        self.timestamp = timestamp
        self.confidence = confidence
        self.coordinates = coordinates
        self.photo_url = photo_url


class Repo:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
        )

    def insert_pothole(self, pothole: Pothole) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pothole (
                    id,
                    device_name,
                    created_on,
                    recorded_on,
                    confidence,
                    latitude,
                    longitude,
                    geohash
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                 """, (
                    str(uuid4()),
                    pothole.device_name,
                    _utc_now(),
                    pothole.timestamp,
                    pothole.confidence,
                    pothole.coordinates[0],
                    pothole.coordinates[1],
                    geohash2.encode(pothole.coordinates[0], pothole.coordinates[1]),
                )
            )

            self.connection.commit()

    def query_potholes_within_bounds(self, bounds: Tuple[float, float, float, float], limit: int) -> List[Pothole]:
        north_east = geohash2.encode(bounds[0], bounds[1])
        south_west = geohash2.encode(bounds[2], bounds[3])

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id,
                       device_name,
                       recorded_on,
                       confidence,
                       latitude,
                       longitude
                FROM pothole
                WHERE geohash BETWEEN %(south_west)s AND %(north_east)s
                ORDER BY random() -- TODO: Find better solution.
                LIMIT %(limit)s
                """, {
                    'north_east': north_east,
                    'south_west': south_west,
                    'limit': limit,
                }
            )

            return list([Pothole(
                id=p[0],
                device_name=p[1],
                timestamp=p[2],
                confidence=p[3],
                coordinates=(p[4], p[5]),
                photo_url=f'https://picsum.photos/seed/{p[0]}/1920/1080',  # TODO: Generate URL based on S3 key.
            ) for p in cursor.fetchall()])
