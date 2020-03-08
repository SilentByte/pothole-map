<!--
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress JSUnresolvedVariable, ES6ModulesDependencies -->
<template>
    <v-autocomplete ref="autocomplete"
                    solo-inverted
                    auto-select-first
                    no-filter
                    hide-no-data
                    hide-selected
                    hide-details
                    clearable
                    return-object
                    spellcheck="false"
                    item-text="description"
                    item-value="placeId"
                    placeholder="Search…"
                    prepend-inner-icon="mdi-magnify"
                    v-model="model"
                    :append-icon="null"
                    :items="items"
                    :search-input.sync="search"
                    @change="onChangePlace"
                    @focus="$emit('focus')"
                    @blur="$emit('blur')" />
</template>

<!--suppress TypeScriptUnresolvedVariable, TypeScriptUnresolvedFunction -->
<script lang="ts">
    /* global google */

    import {
        Component,
        Prop,
        Vue,
        Watch,
    } from "vue-property-decorator";

    import * as geo from "@/modules/geo";

    interface IPlacePrediction {
        placeId: string;
        description: string;
    }

    @Component
    export default class AddressAutocomplete extends Vue {
        @Prop({type: Object, default: () => null}) biasCoordinates!: geo.IPoint | null;

        model = null;
        items: IPlacePrediction[] = [];
        search = "";
        sessionToken = "";

        autocompleteService: any = null;
        placesService: any = null;
        pending = true;

        @Watch("search")
        async onSearch() {
            if(!this.search || this.pending) {
                return;
            }

            this.pending = true;

            const bias: any = {};
            if(this.biasCoordinates) {
                bias.location = new google.maps.LatLng(this.biasCoordinates.lat, this.biasCoordinates.lng);
                bias.radius = 100000;
            }

            this.autocompleteService.getQueryPredictions({
                input: this.search,
                sessionToken: this.sessionToken,
                language: "en",
                ...bias,
            }, (predictions: any[], status: any) => {
                this.pending = false;
                if(status !== google.maps.places.PlacesServiceStatus.OK) {
                    return;
                }

                this.items = predictions.map(p => ({
                    placeId: p.place_id,
                    description: p.description,
                }));
            });
        }

        onChangePlace(prediction: IPlacePrediction) {
            if(!prediction) {
                return;
            }

            this.pending = true;
            this.placesService.getDetails({
                placeId: prediction.placeId,
                sessionToken: this.sessionToken,
                fields: ["geometry"],
            }, (details: any, status: any) => {
                this.pending = false;
                this.sessionToken = new google.maps.places.AutocompleteSessionToken();

                if(status !== google.maps.places.PlacesServiceStatus.OK) {
                    return;
                }

                // noinspection TypeScriptValidateJSTypes
                const place: geo.IPlace = {
                    placeId: prediction.placeId,
                    description: prediction.description,
                    coordinates: geo.point(details.geometry.location.lat(), details.geometry.location.lng()),
                };

                this.$emit("address-selected", place);
                (document as any).activeElement.blur();
            });
        }

        mounted() {
            (this as any).$gmapApiPromiseLazy({}).then(() => {
                this.sessionToken = new google.maps.places.AutocompleteSessionToken();
                this.autocompleteService = new google.maps.places.AutocompleteService();
                this.placesService = new google.maps.places.PlacesService(document.createElement("div"));
            }).finally(() => this.pending = false);
        }
    }
</script>

<style lang="scss" scoped>
    //
</style>
