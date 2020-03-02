/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

export function postpone(handler: () => void) {
    setTimeout(handler, 0);
}
