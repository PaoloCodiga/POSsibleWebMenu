/** @odoo-module **/

import { describe, expect, test } from "@odoo/hoot";
import { PossibleWebMenuConfigurationDialog } from "@possible_web_menu/website_builder/possible_web_menu_configuration_dialog";

function createDialogState(overrides = {}) {
    const dialog = Object.create(PossibleWebMenuConfigurationDialog.prototype);
    dialog.state = {
        pricelists: [{ id: 12, name: "Website pricelist" }],
        pricelistId: 12,
        selectedCategoryIds: [3],
        categorySearch: "",
        validationRequested: false,
        validationMessage: "",
        ...overrides,
    };
    return dialog;
}

describe("possible web menu builder configuration", () => {
    test("keeps canonical initial values and validates an allowed pricelist", () => {
        globalThis.__possibleWebMenuHootExecuted = true;
        const dialog = createDialogState();

        expect(dialog.isPricelistValid).toBe(true);
        expect(dialog.isCategorySelected(3)).toBe(true);
        expect(dialog.categoryIndent({ depth: 2 })).toBe("padding-inline-start: 2.5rem;");
        dialog.validateConfiguration();

        expect(dialog.state.validationRequested).toBe(true);
        expect(Boolean(dialog.state.validationMessage)).toBe(true);
    });

    test("updates only the local category selection and rejects an unavailable pricelist", () => {
        const dialog = createDialogState({ pricelistId: 999, selectedCategoryIds: [5, 3] });

        dialog.toggleCategory({ currentTarget: { value: "7", checked: true } });
        expect(dialog.state.selectedCategoryIds).toEqual([3, 5, 7]);
        dialog.toggleCategory({ currentTarget: { value: "5", checked: false } });
        expect(dialog.state.selectedCategoryIds).toEqual([3, 7]);
        dialog.validateConfiguration();

        expect(dialog.isPricelistValid).toBe(false);
        expect(dialog.state.validationRequested).toBe(true);
        expect(dialog.state.validationMessage).toBe("");
    });
});
