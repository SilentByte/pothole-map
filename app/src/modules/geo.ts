/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

export interface IPoint {
    lat: number;
    lng: number;
}

export interface IMarker {
    id: string;
    coordinates: IPoint;
    iconUrl?: string;
}

export interface IPlace {
    placeId: string;
    description: string;
    coordinates: IPoint;
}

export interface IBounds {
    northEast: IPoint;
    southWest: IPoint;
}

export interface IMapViewOptions {
    coordinates: IPoint;
    zoom: number;
}

export function point(latitude: number, longitude: number): IPoint {
    return {
        lat: latitude,
        lng: longitude,
    };
}

export async function getUserLocation(): Promise<IPoint> {
    if(!navigator.geolocation) {
        throw new Error("Geolocation API is not available");
    }

    const position: any = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject);
    });

    return point(position.coords.latitude, position.coords.longitude);
}

export function extractMapViewOptions(text: string): IMapViewOptions | null {
    const matches = /@(-?\d+(\.\d+)?),(-?\d+(\.\d+)?),(\d+(\.\d+)?)z/.exec(text);
    if(!matches) {
        return null;
    }

    return {
        coordinates: point(parseFloat(matches[1]), parseFloat(matches[3])),
        zoom: parseFloat(matches[5]),
    };
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
