/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import axios, { AxiosInstance } from "axios";

const REQUEST_TIMEOUT_MS = 1000 * 30;

export function rest(): AxiosInstance {
    // noinspection TypeScriptUnresolvedVariable
    return axios.create({
        baseURL: process.env.VUE_APP_API_URL || "/",
        withCredentials: false,
        timeout: REQUEST_TIMEOUT_MS,
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    });
}
