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

            <span class="title ml-3 mr-5 text-uppercase">Pothole<span class="font-weight-light">Map</span></span>

            <v-text-field solo-inverted
                          flat
                          hide-details
                          label="Search…"
                          prepend-inner-icon="mdi-magnify" />

            <v-spacer />
        </v-app-bar>

        <v-navigation-drawer app clipped
                             v-model="drawer">
            <v-layout column fill-height>
                <v-list nav dense>
                    <v-list-item link>
                        <v-list-item-icon>
                            <v-icon>mdi-map-marker</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>Pothole Map</v-list-item-title>
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

    // import { getModule } from "vuex-module-decorators";
    // import { AppModule } from "@/store/app";

    // const appState = getModule(AppModule);

    @Component
    export default class App extends Vue {
        drawer = null;
    }
</script>

<style lang="scss">
    html {
        overflow-y: hidden;
    }
</style>
