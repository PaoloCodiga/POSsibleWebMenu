/** @odoo-module **/

import { clickOnSave, registerWebsitePreviewTour } from "@website/js/tours/tour_utils";

registerWebsitePreviewTour(
    "possible_web_menu_builder_persistence",
    {
        url: "/b3-builder-persistence",
        edition: true,
    },
    () => [
        {
            trigger: ":iframe .s_possible_web_menu .s_possible_web_menu_content",
        },
        {
            trigger: ":iframe .s_possible_web_menu_title",
            run: "editor B3 Builder Menu Saved",
        },
        {
            trigger: ':iframe .s_possible_web_menu_title:contains("B3 Builder Menu Saved")',
        },
        ...clickOnSave(),
    ]
);
