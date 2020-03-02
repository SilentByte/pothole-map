/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import {
    VuexModule,
    Module,
} from "vuex-module-decorators";

import store from "@/store";
import { IPothole } from "@/store/models";

@Module({
    store,
    dynamic: true,
    namespaced: true,
    name: "app",
})
export class AppModule extends VuexModule {
    potholes: IPothole[] = [{
        id: "139c57b0-628a-4bd1-acee-5893a697de6b",
        deviceName: "Test Device 01",
        timestamp: new Date(),
        confidence: 0.5,
        coordinates: [-31.934390853103174, 115.81598281860352],
        photoUrl: "https://picsum.photos/seed/01/1920/1080?random=1",
    }, {
        id: "2e69f436-495b-450c-884e-abe414dcc402",
        deviceName: "Test Device 02",
        timestamp: new Date(),
        confidence: 0.5,
        coordinates: [-31.919093057279348, 115.84928512573241],
        photoUrl: undefined,
    }, {
        id: "1a73b00b-1c88-46fb-a619-771c6abb2686",
        deviceName: "Test Device 03",
        timestamp: new Date(),
        confidence: 0.5,
        coordinates: [-31.914503222291746, 115.82714080810547],
        photoUrl: "https://picsum.photos/seed/03/1920/1080?random=3",
    }, {
        id: "bf4b99c3-e491-4425-9578-bb7750ebc35e",
        deviceName: "Test Device 04",
        timestamp: new Date(),
        confidence: 0.5,
        coordinates: [-31.943131307956442, 115.8295440673828],
        photoUrl: "https://picsum.photos/seed/04/1920/1080?random=4",
    }, {
        id: "18e9468d-3dd6-47c4-a63a-ba0aa9ea923e",
        deviceName: "Test Device 05",
        timestamp: new Date(),
        confidence: 0.5,
        coordinates: [-31.958279460482014, 115.84404945373534],
        photoUrl: "https://picsum.photos/seed/05/1920/1080?random=5",
    }];
}
