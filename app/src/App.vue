<!--
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->
<template>
    <v-app>
        <v-app-bar app dark
                   clipped-left
                   color="primary">

            <v-app-bar-nav-icon @click="drawer = !drawer" />

            <span v-if="!$vuetify.breakpoint.xs || !addressFocused"
                  class="title ml-3 mr-5 text-uppercase">
                Pothole<span class="font-weight-light">Map</span>
            </span>

            <AddressAutocomplete :bias-coordinates="mapCenter"
                                 @address-selected="onAddressSelected"
                                 @focus="addressFocused = true"
                                 @blur="addressFocused = false" />

            <v-btn icon
                   :loading="userLocationPending"
                   @click="onCenterOnUserLocation">
                <v-icon>mdi-crosshairs-gps</v-icon>
            </v-btn>

            <v-spacer />
        </v-app-bar>

        <v-navigation-drawer app clipped
                             v-model="drawer">
            <v-layout column fill-height>
                <v-list nav dense>
                    <v-list-item link exact :to="{ name: 'MapView' }">
                        <v-list-item-icon>
                            <v-icon>mdi-map-marker</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>Pothole Map</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                    <v-list-item link :to="{ name: 'AboutView' }">
                        <v-list-item-icon>
                            <v-icon>mdi-emoticon</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>What's This?</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>

                <v-spacer />

                <v-list nav dense>
                    <v-list-item>
                        <v-layout row justify-center>
                            <v-btn small text
                                   href="https://twitter.com/RicoBeti"
                                   target="_blank"
                                   class="text-none"
                                   color="primary">
                                @RicoBeti
                            </v-btn>
                            <v-btn small text
                                   href="https://twitter.com/Phtevem"
                                   target="_blank"
                                   class="text-none"
                                   color="primary">
                                @Phtevem
                            </v-btn>
                        </v-layout>
                    </v-list-item>
                </v-list>
            </v-layout>
        </v-navigation-drawer>

        <v-content>
            <router-view />
        </v-content>
    </v-app>
</template>

<script lang="ts">
    import {
        Component,
        Vue,
    } from "vue-property-decorator";

    import AddressAutocomplete from "@/components/AddressAutocomplete.vue";

    import { IPlace } from "@/modules/geo";

    import { getModule } from "vuex-module-decorators";
    import { AppModule } from "@/store/app";

    const appState = getModule(AppModule);

    @Component({
        components: {AddressAutocomplete},
    })
    export default class App extends Vue {
        drawer = null;
        addressFocused = false;

        get userLocationPending() {
            return appState.mapUserLocationPending;
        }

        get mapCenter() {
            return appState.mapCenter;
        }

        onCenterOnUserLocation() {
            this.$router.push({name: "MapView"});
            appState.doCenterOnUserLocation();
        }

        onAddressSelected(place: IPlace) {
            this.$router.push({name: "MapView"});
            appState.doCenterOnLocation({
                center: place.coordinates,
            });
        }
    }
</script>

<style lang="scss">
    html {
        overflow-y: auto;
    }
</style>
