<!--
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<template>
    <v-container class="pa-5 text-center content">
        <h2 class="mb-3 display-2 text-uppercase">
            Here's a <span class="text-primary">Quick</span> Overview
        </h2>

        <div class="body-1">
            TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO.
            TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO.
            TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO.
            TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO.
            TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO.
            TODO. TODO. TODO. TODO. TODO. TODO. TODO. TODO.
        </div>


        <h2 class="mb-3 display-2 text-uppercase text-primary">
            #potholemap
        </h2>

        <v-layout row>
            <v-flex xs12 sm4 px-3>
                <v-btn x-large block dark color="#4267b2">
                    <v-icon left>mdi-facebook</v-icon>
                    Share
                </v-btn>
            </v-flex>

            <v-flex xs12 sm4 px-3>
                <v-btn x-large block dark color="#1da1f2">
                    <v-icon left>mdi-twitter</v-icon>
                    Tweet
                </v-btn>
            </v-flex>

            <v-flex xs12 sm4 px-3>
                <v-btn x-large block dark color="#424242">
                    <v-icon left>mdi-email</v-icon>
                    Send
                </v-btn>
            </v-flex>
        </v-layout>

        <div class="twitter-feed">
            <a class="twitter-timeline"
               href="https://twitter.com/RicoBeti"
               data-tweet-limit="1"
               data-chrome="noheader, nofooter, noborders, transparent, noscrollbar">
                Tweets by @RicoBeti
            </a>
        </div>

        <h2 class="mb-3 display-2 text-uppercase">
            Want to get in touch?
        </h2>

        <div class="body-1">
            Follow us on <span class="text-primary">Twitter</span> and <span class="text-primary">Github</span> to find
            out what other projects we're working and feel free to drop us a message if you have any questions!
        </div>

        <v-layout row my-5 py-5>
            <v-flex xs12 sm6 px-3>
                <v-btn dark
                       color="#1da1f2"
                       class="text-none"
                       href="https://twitter.com/RicoBeti"
                       target="_blank">
                    <v-icon left>mdi-twitter</v-icon>
                    @RicoBeti
                </v-btn>
                /
                <v-btn dark
                       color="#333"
                       class="text-none"
                       href="https://github.com/SilentByte"
                       target="_blank">
                    <v-icon left>mdi-github</v-icon>
                    @SilentByte
                </v-btn>
            </v-flex>

            <v-flex xs12 sm6 px-3>
                <v-btn dark
                       color="#1da1f2"
                       class="text-none"
                       href="https://twitter.com/Phtevem"
                       target="_blank">
                    <v-icon left>mdi-twitter</v-icon>
                    @Phtevem
                </v-btn>
                /
                <v-btn dark
                       color="#333"
                       class="text-none"
                       href="https://github.com/SrzStephen"
                       target="_blank">
                    <v-icon left>mdi-github</v-icon>
                    @SrzStephen
                </v-btn>
            </v-flex>
        </v-layout>

        <v-footer absolute padless>
            <v-card flat tile
                    width="100%"
                    class="primary">
                <v-card-text class="white--text">
                    Copyright &copy; {{ new Date().getFullYear() }} by
                    <a href="https://silentbyte.com"
                       target="_blank"
                       style="color: white; font-weight: bold; text-decoration: none">
                        SilentByte
                    </a>
                </v-card-text>
            </v-card>
        </v-footer>
    </v-container>
</template>

<script lang="ts">
    import {
        Component,
        Vue,
    } from "vue-property-decorator";

    @Component
    export default class AboutView extends Vue {
        mounted() {
            // Send simple ping without coordinates for privacy reasons.
            this.$gtag.pageview({
                "page_title": "AboutView",
                "page_path": "/about",
                "page_location": "/",
            });
        }
    }
</script>

<style lang="scss" scoped>
    .text-primary {
        color: #3f51b5
    }

    .content {
        max-width: 1000px;
        margin-bottom: 6em;

        h2 {
            padding: 2em 0 0.5em 0;

            &:first-child {
                padding-top: 1em;
            }
        }

        .body-1 {
            font-size: 1.3rem !important;
            line-height: 1.5em !important;
        }

        .twitter-feed {
            margin: 3em 0;
        }

        .footer {
            margin-top: 3em !important;
        }
    }
</style>
