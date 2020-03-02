<!--
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->
<template>
    <v-container ma-0 pa-0 fluid fill-height>
        <gmap-map map-type-id="roadmap"
                  style="width: 100%; height: 100%"
                  :zoom="zoom"
                  :center="center"
                  :options="options">

            <gmap-marker v-for="m in markers"
                         :key="m.id"
                         :position="m.coordinates"
                         :icon="m.iconUrl" />
        </gmap-map>
    </v-container>
</template>

<script lang="ts">
    import {
        Component,
        Vue,
    } from "vue-property-decorator";

    import * as geo from "@/modules/geo";
    import { Marker } from "@/modules/geo";

    @Component
    export default class MapView extends Vue {
        zoom = 12;
        center = geo.point(-31.9440151, 115.8901276);
        options = geo.MAP_OPTIONS;
        markers: Marker[] = [];
    }
</script>
