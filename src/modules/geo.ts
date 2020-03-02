/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

export interface Point {
    lat: number;
    lng: number;
}

export interface Marker {
    id: string;
    coordinates: Point;
    iconUrl?: string;
}

export interface MarkerOptions {
    id: string;
    coordinates: Point;
    iconUrl?: string;
}

export interface Place {
    placeId: string;
    description: string;
    coordinates: Point;
}

export function point(latitude: number, longitude: number): Point {
    return {
        lat: latitude,
        lng: longitude,
    };
}

export function marker(options: MarkerOptions): Marker {
    return {
        id: options.id,
        coordinates: options.coordinates,
        iconUrl: options.iconUrl || "",
    }
}

export async function getUserLocation(): Promise<Point> {
    if(!navigator.geolocation) {
        throw new Error("Geolocation API is not available");
    }

    const position: any = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject);
    });

    return point(position.coords.latitude, position.coords.longitude);
}

export const MAP_OPTIONS = {
    styles: [
        {
            "featureType": "administrative.land_parcel",
            "elementType": "labels",
            "stylers": [
                {
                    "visibility": "off",
                },
            ],
        },
        {
            "featureType": "poi",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "off",
                },
            ],
        },
        {
            "featureType": "poi.business",
            "stylers": [
                {
                    "visibility": "off",
                },
            ],
        },
        {
            "featureType": "poi.park",
            "elementType": "labels.text",
            "stylers": [
                {
                    "visibility": "off",
                },
            ],
        },
        {
            "featureType": "road.local",
            "elementType": "labels",
            "stylers": [
                {
                    "visibility": "off",
                },
            ],
        },
    ],
};
