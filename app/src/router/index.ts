/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import Vue from "vue";
import VueRouter from "vue-router";
import MapView from "@/views/MapView.vue";

Vue.use(VueRouter);

const routes = [
    {
        path: "/:options(@[\\-0-9\\.\\,]+z)?",
        name: "MapView",
        component: MapView,
    },
    {
        path: "*",
        redirect: "/",
    },
];

const router = new VueRouter({
    base: process.env.BASE_URL,
    mode: "history",
    routes,
});

export default router;
