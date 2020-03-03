/*
 * Pothole Map
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

type PrimitiveTypes = "boolean" | "number" | "string";

function throwOnUndefinedOrNull(value: any) {
    if(value === undefined || value === null) {
        console.trace("Value expected, received null or undefined");
        throw new Error("Value expected, received null or undefined");
    }
}

function throwOnWrongType(value: any, type: PrimitiveTypes) {
    throwOnUndefinedOrNull(value);

    if(typeof value !== type) {
        console.trace(`Type '${type}' expected, received ${typeof value} for value:`);
        console.trace(value);
        throw new Error(`Type '${type}' expected, received ${typeof value}`);
    }
}

export function boolean(value: any): boolean {
    throwOnWrongType(value, "boolean");
    return value;
}

export function number(value: any): number {
    throwOnWrongType(value, "number");
    return value;
}

export function integer(value: any): number {
    throwOnWrongType(value, "number");

    if(!Number.isInteger(value)) {
        throw new Error("Number is not an integer");
    }

    return value;
}

export function string(value: any): string {
    throwOnWrongType(value, "string");
    return value;
}

export function date(value: any): Date {
    if(value instanceof Date) {
        return value as Date;
    }

    throwOnWrongType(value, "string");
    return new Date(value);
}

export function array(value: any): unknown[] {
    if(!Array.isArray(value)) {
        throw new Error("Array expected");
    }

    return value;
}

export function uuid(value: any): string {
    throwOnWrongType(value, "string");

    if(!/^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$/.test(value)) {
        throw new Error("UUID expected");
    }

    return value;
}

export function optional<T>(value: any, validator: (value: any) => T): T | undefined {
    if(value === null || value === undefined) {
        return undefined;
    }

    return validator(value);
}


