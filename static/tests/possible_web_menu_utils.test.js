/** @odoo-module **/
import { describe, expect, test } from "@odoo/hoot";
import { DEFAULT_CONFIG, normalizeDataset, parseBoolean, parseCategoryIds, parsePositiveInteger, payloadFromConfig } from "@possible_web_menu/snippets/s_possible_web_menu/possible_web_menu_utils";

describe("possible web menu configuration utilities", () => {
    test("parses strict booleans and positive integers", () => {
        expect(parseBoolean("true", false)).toBe(true);
        expect(parseBoolean("false", true)).toBe(false);
        expect(parseBoolean("yes", true)).toBe(true);
        expect(parsePositiveInteger("12")).toBe(12);
        expect(parsePositiveInteger("-1")).toBe(null);
    });
    test("normalizes category IDs and omits arbitrary dataset values", () => {
        expect(parseCategoryIds("3, 2,3,invalid")).toEqual([2, 3]);
        const config = normalizeDataset({ pricelistId: "7", posCategoryIds: "4,2,4", filterSale: "false", layout: "invalid", domain: "unsafe" });
        expect(config.pricelistId).toBe(7);
        expect(config.posCategoryIds).toEqual([2, 4]);
        expect(config.filterSale).toBe(false);
        expect(config.layout).toBe(DEFAULT_CONFIG.layout);
        expect(payloadFromConfig(config)).not.toHaveProperty("domain");
    });
});
