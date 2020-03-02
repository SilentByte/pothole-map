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

import store from "@/store";

@Module({
    store,
    dynamic: true,
    namespaced: true,
    name: "app",
})
export class AppModule extends VuexModule {
    testCounter = 0;

    @Mutation
    increaseCounter() {
        this.testCounter += 1;
    }

    @Action({rawError: true})
    async doFoo() {
        //
    }
}
