<!--
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress HtmlUnknownTarget -->
<template>
    <v-container ma-0 pa-0 fluid fill-height>
        <gmap-map ref="map"
                  map-type-id="roadmap"
                  style="width: 100%; height: 100%"
                  :zoom="zoom"
                  :center="center"
                  :options="options"
                  @idle="onIdle"
                  @bounds_changed="onBoundsChanged">

            <gmap-marker v-if="userMarker"
                         :position="userMarker.coordinates"
                         :icon="userMarker.iconUrl" />

            <gmap-cluster :minimum-cluster-size="5"
                          :zoom-on-click="true"
                          :styles="clusterStyles">
                <gmap-marker v-for="m in markers"
                             :key="m.id"
                             :position="m.coordinates"
                             :icon="m.iconUrl"
                             @click="onMarkerClick(m.id)" />
            </gmap-cluster>
        </gmap-map>

        <v-bottom-sheet inset
                        hide-overlay
                        max-width="800"
                        v-model="sheet">
            <v-sheet>
                <v-card>
                    <v-layout d-flex flex-no-wrap>
                        <v-hover v-slot:default="{ hover }">
                            <v-avatar flat tile
                                      size="150"
                                      class="ma-3 pothole-thumbnail"
                                      @click="onPreviewPhoto">
                                <v-img v-if="currentPothole.photoUrl"
                                       :key="currentPothole.id"
                                       :src="currentPothole.photoUrl">
                                    <template v-slot:placeholder>
                                        <v-row class="fill-height ma-0"
                                               align="center"
                                               justify="center">
                                            <v-progress-circular indeterminate
                                                                 color="primary" />
                                        </v-row>
                                    </template>

                                    <v-fade-transition>
                                        <v-layout v-if="hover"
                                                  d-flex
                                                  justify-center align-center
                                                  transition-fast-in-fast-out
                                                  style="background: rgba(0, 0, 0, 0.4)">
                                            <v-icon x-large
                                                    color="white">
                                                mdi-magnify-plus
                                            </v-icon>
                                        </v-layout>
                                    </v-fade-transition>
                                </v-img>
                                <v-img v-else src="@/assets/logo.png" />
                            </v-avatar>
                        </v-hover>

                        <div>
                            <v-card-title class="headline">
                                {{ currentPothole.coordinates[0].toFixed(6) }},
                                {{ currentPothole.coordinates[1].toFixed(6) }}
                            </v-card-title>
                            <v-card-subtitle class="pb-1">
                                {{ currentPothole.deviceName }},
                                {{ (currentPothole.confidence * 100).toFixed(0) }}%,
                                {{ currentPothole.timestamp.toLocaleString() }}
                            </v-card-subtitle>
                        </div>

                        <v-spacer />

                        <v-btn icon
                               color="primary"
                               class="ma-2"
                               @click="sheet = false">
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                    </v-layout>
                </v-card>
            </v-sheet>
        </v-bottom-sheet>

        <v-dialog v-model="photoPreview"
                  :max-width="$vuetify.breakpoint.name === 'sm' ? '100%' : '80%'">
            <v-card flat>
                <v-img v-if="currentPothole.photoUrl"
                       contain
                       :max-height="$vuetify.breakpoint.name === 'sm' ? '100%' : '80%'"
                       :key="currentPothole.id"
                       :src="currentPothole.photoUrl"
                       @click="photoPreview = false">
                    <template v-slot:placeholder>
                        <v-row class="fill-height ma-0"
                               align="center"
                               justify="center">
                            <v-progress-circular indeterminate
                                                 color="primary" />
                        </v-row>
                    </template>
                </v-img>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<!--suppress TypeScriptUnresolvedVariable, TypeScriptUnresolvedFunction -->
<script lang="ts">
    import _ from "lodash";

    import {
        Component,
        Vue,
    } from "vue-property-decorator";
    import { getModule } from "vuex-module-decorators";

    import * as geo from "@/modules/geo";
    import { IMarker } from "@/modules/geo";

    import { postpone } from "@/modules/utils";

    import { AppModule } from "@/store/app";
    import { IPothole } from "@/store/models";

    const appState = getModule(AppModule);

    const debouncedDoFetchPotholes = _.debounce(appState.doFetchPotholes, 100);

    @Component
    export default class MapView extends Vue {
        options = geo.MAP_OPTIONS;
        sheet = false;
        photoPreview = false;

        currentPothole: IPothole = {
            id: "",
            deviceName: "",
            timestamp: new Date(),
            confidence: 0,
            coordinates: [0, 0],
            photoUrl: undefined,
        };

        clusterStyles = [
            {
                url: "./images/markers/m1.svg",
                height: 32,
                width: 32,
                anchor: [16, 16],
                textColor: "#fff",
                textSize: 10,
            },
            {
                url: "./images/markers/m2.svg",
                height: 50,
                width: 50,
                anchor: [25, 25],
                textColor: "#fff",
                textSize: 12,
            },
        ];

        get center() {
            return appState.mapCenter;
        }

        get zoom() {
            return appState.mapZoom;
        }

        get userMarker(): IMarker | null {
            if(!appState.mapUserMarker) {
                return null;
            }

            return {
                id: "user-marker",
                coordinates: appState.mapUserMarker,
            };
        }

        get markers(): IMarker[] {
            return appState.potholes.map(p => ({
                id: p.id,
                coordinates: geo.point(p.coordinates[0], p.coordinates[1]),
                iconUrl: "/images/markers/pothole.svg",
            }));
        }

        async onIdle() {
            const map = await (this.$refs.map as any).$mapPromise;

            appState.setMapZoom(map.getZoom());
            appState.setMapCenter({
                lat: map.getCenter().lat(),
                lng: map.getCenter().lng(),
            });

            const bounds = map.getBounds();
            await debouncedDoFetchPotholes({
                northEast: geo.point(bounds.getNorthEast().lat(), bounds.getNorthEast().lng()),
                southWest: geo.point(bounds.getSouthWest().lat(), bounds.getSouthWest().lng()),
            });
        }

        async onBoundsChanged() {
            const map = await (this.$refs.map as any).$mapPromise;

            const latitude = map.getCenter().lat().toFixed(7);
            const longitude = map.getCenter().lng().toFixed(7);
            const zoom = map.getZoom().toFixed(2);

            const options = `@${latitude},${longitude},${zoom}z`;
            if(this.$route.params.options !== options) {
                await this.$router.replace({
                    name: "MapView",
                    params: {
                        options,
                    },
                });
            }
        }

        onMarkerClick(markerId: string) {
            postpone(() => {
                this.sheet = true;
                this.currentPothole = appState.potholes.find(p => p.id === markerId) as IPothole;
            });
        }

        onPreviewPhoto() {
            if(this.currentPothole.photoUrl) {
                this.photoPreview = true;
            }
        }

        mounted() {
            if(this.$route.params.options) {
                const options = geo.extractMapViewOptions(this.$route.params.options);
                if(options) {
                    appState.setMapZoom(options.zoom);
                    appState.setMapCenter(options.coordinates);
                }
            }
        }
    }
</script>

<style lang="scss">
    .pothole-thumbnail {
        cursor: pointer !important;
    }
</style>
