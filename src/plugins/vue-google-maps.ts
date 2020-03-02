/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import Vue from "vue";
import * as VueGoogleMaps from "vue2-google-maps";

// noinspection TypeScriptUnresolvedVariable
Vue.use(VueGoogleMaps as any, {
    load: {
        key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY,
        libraries: "drawing,geometry,places",
        language: "en",
        region: "us",
    },

    installComponents: true,
});
