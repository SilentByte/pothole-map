/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

export interface IPothole {
    id: string;
    deviceName: string;
    timestamp: Date;
    confidence: number;
    coordinates: [number, number];
    photoUrl?: string;
}
