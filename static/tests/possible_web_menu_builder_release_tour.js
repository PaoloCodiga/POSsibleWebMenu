/** @odoo-module **/

import {
    clickOnSave,
    clickOnSnippet,
    insertSnippet,
    registerWebsitePreviewTour,
} from "@website/js/tours/tour_utils";

registerWebsitePreviewTour(
    "possible_web_menu_builder_release",
    {
        url: "/c3-builder-release",
        edition: true,
    },
    () => [
        ...insertSnippet({ groupName: "POSsible", name: "POS Web Menu", id: "s_possible_web_menu" }),
        ...clickOnSnippet({ id: "s_possible_web_menu" }),
        {
            trigger: 'button:contains("Configure menu")',
            run: "click",
        },
        {
            trigger: "#possible_web_menu_pricelist",
            run() {
                const option = [...this.anchor.options].find((item) =>
                    item.textContent.includes("C3 Release Pricelist")
                );
                if (!option) {
                    throw new Error("The C3 fixture pricelist is not available in the configuration dialog.");
                }
                this.anchor.value = option.value;
                this.anchor.dispatchEvent(new Event("change", { bubbles: true }));
            },
        },
        {
            trigger: 'label:contains("C3 Release Category") input',
            run: "click",
        },
        {
            trigger: "#possible_web_menu_layout",
            run: "select two_columns",
        },
        {
            trigger: 'button:contains("Apply configuration")',
            run: "click",
        },
        {
            trigger: ':iframe .s_possible_web_menu[data-pricelist-id]:not([data-pricelist-id=""])[data-pos-category-ids]:not([data-pos-category-ids=""])[data-layout="two_columns"]',
        },
        {
            trigger: ':iframe .o_possible_web_menu_product_name:contains("C3 Release Visible Product")',
        },
        {
            trigger: ".o-website-builder_sidebar .fa-undo:not([disabled])",
            run: "click",
        },
        {
            trigger: ':iframe .s_possible_web_menu[data-pricelist-id=""][data-pos-category-ids=""][data-layout="leaders"]',
        },
        {
            trigger: ".o-website-builder_sidebar .fa-repeat:not([disabled])",
            run: "click",
        },
        {
            trigger: ':iframe .s_possible_web_menu[data-pricelist-id]:not([data-pricelist-id=""])[data-pos-category-ids]:not([data-pos-category-ids=""])[data-layout="two_columns"]',
        },
        ...clickOnSave(),
    ]
);
