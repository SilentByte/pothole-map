/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import {
    VuexModule,
    Module,
    Mutation,
    Action,
} from "vuex-module-decorators";

import * as ensure from "@/modules/ensure";
import * as geo from "@/modules/geo";
import { IBounds, IPoint } from "@/modules/geo";
import { rest } from "@/modules/api";

import store from "@/store";
import { IPothole } from "@/store/models";

function coordinatesFromAny(data: any): [number, number] {
    data = ensure.array(data);
    return [ensure.number(data[0]), ensure.number(data[1])];
}

function potholeFromAny(data: any): IPothole {
    return {
        id: ensure.uuid(data.id),
        deviceName: ensure.string(data.deviceName),
        timestamp: ensure.date(data.timestamp),
        confidence: ensure.number(data.confidence),
        coordinates: coordinatesFromAny(data.coordinates),
        photoUrl: ensure.optional(data.photoUrl, ensure.string),
    };
}

@Module({
    store,
    dynamic: true,
    namespaced: true,
    name: "app",
})
export class AppModule extends VuexModule {
    mapCenter: IPoint = geo.point(-31.9440151, 115.8901276);
    mapZoom = 12;
    mapUserMarker: IPoint | null = null;
    mapUserLocationPending = false;

    potholes: IPothole[] = [];

    @Mutation
    setMapCenter(center: IPoint) {
        this.mapCenter = center;
    }

    @Mutation
    setMapZoom(zoom: number) {
        this.mapZoom = zoom;
    }

    @Mutation
    setUserMarker(center: IPoint | null) {
        this.mapUserMarker = center;
    }

    @Mutation
    setMapPendingUserLocation(state: boolean) {
        this.mapUserLocationPending = state;
    }

    @Mutation
    setPotholes(potholes: IPothole[]) {
        this.potholes = potholes;
    }

    @Action({rawError: true})
    doCenterOnUserLocation() {
        this.setMapPendingUserLocation(true);
        geo.getUserLocation()
            .then(center => {
                this.setMapCenter(center);
                this.setMapZoom(12);
                this.setUserMarker(center);
            })
            .finally(() => this.setMapPendingUserLocation(false));
    }

    @Action({rawError: true})
    doCenterOnLocation(center: IPoint) {
        this.setMapCenter(center);
        this.setMapZoom(15);
        this.setUserMarker(center);
    }

    @Action({rawError: true})
    async doFetchPotholes(bounds: IBounds) {
        const response = await rest().get("potholes", {
            params: {
                nelat: bounds.northEast.lat,
                nelng: bounds.northEast.lng,
                swlat: bounds.southWest.lat,
                swlng: bounds.southWest.lng,
            },
        });

        this.setPotholes(response.data.map(potholeFromAny));
    }
}
