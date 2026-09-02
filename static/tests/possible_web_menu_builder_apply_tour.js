/** @odoo-module **/

import { clickOnSnippet, registerWebsitePreviewTour } from "@website/js/tours/tour_utils";

registerWebsitePreviewTour(
    "possible_web_menu_builder_apply",
    {
        url: "/c2-builder-apply",
        edition: true,
    },
    () => [
        ...clickOnSnippet({ id: "s_possible_web_menu" }),
        {
            trigger: 'button:contains("Configure menu")',
            run: "click",
        },
        {
            trigger: "#possible_web_menu_layout",
            run: "select two_columns",
        },
        {
            trigger: 'label:contains("Show description") input',
            run: "click",
        },
        {
            trigger: 'button:contains("Apply configuration")',
            run: "click",
        },
        {
            trigger: ':iframe .s_possible_web_menu[data-layout="two_columns"][data-show-description="true"]',
        },
        {
            trigger: ':iframe .o_possible_web_menu_product_name:contains("C2 Builder Visible Product")',
        },
        {
            trigger: ".o-website-builder_sidebar .fa-undo:not([disabled])",
            run: "click",
        },
        {
            trigger: ':iframe .s_possible_web_menu[data-layout="leaders"][data-show-description="false"]',
        },
        {
            trigger: ".o-website-builder_sidebar .fa-repeat:not([disabled])",
            run: "click",
        },
        {
            trigger: ':iframe .s_possible_web_menu[data-layout="two_columns"][data-show-description="true"]',
        },
    ]
);
