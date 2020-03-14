/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import Vue from "vue";
import VueGtag from "vue-gtag";

Vue.use(VueGtag, {
    config: {id: process.env.VUE_APP_GOOGLE_ANALYTICS_KEY},
    "send_page_view": false,
});
