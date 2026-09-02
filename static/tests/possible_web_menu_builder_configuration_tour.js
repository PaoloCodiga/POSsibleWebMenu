/** @odoo-module **/

import { clickOnSnippet, registerWebsitePreviewTour } from "@website/js/tours/tour_utils";

registerWebsitePreviewTour(
    "possible_web_menu_builder_configuration",
    {
        url: "/c1-builder-configuration",
        edition: true,
    },
    () => [
        ...clickOnSnippet({ id: "s_possible_web_menu" }),
        {
            trigger: 'button:contains("Configure menu")',
            run: "click",
        },
        {
            trigger: "#possible_web_menu_pricelist",
        },
        {
            trigger: '#possible_web_menu_pricelist option:not(:visible):contains("C1 Browser Pricelist")',
        },
        {
            trigger: '#possible_web_menu_pricelist option:checked:not(:visible):contains("C1 Browser Pricelist")',
        },
        {
            trigger: 'label:contains("C1 Browser Category") input:checked',
        },
        {
            trigger: 'p:contains("Product filters")',
        },
        {
            trigger: 'label:contains("Show description")',
        },
        {
            trigger: 'label:contains("Sort products by")',
        },
        {
            trigger: 'label:contains("Layout")',
        },
        {
            trigger: 'button:contains("Validate configuration")',
            run: "click",
        },
        {
            trigger: '.alert-success:contains("Configuration is valid")',
        },
        {
            trigger: 'button:contains("Cancel")',
            run: "click",
        },
    ]
);
