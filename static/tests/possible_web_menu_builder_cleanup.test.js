/** @odoo-module **/

import { describe, expect, getFixture, test } from "@odoo/hoot";
import { cleanPossibleWebMenuForSave } from "@possible_web_menu/website_builder/possible_web_menu_option_plugin";

const markup = `<section class="s_possible_web_menu" data-pricelist-id="7" data-layout="two_columns"><h2 class="s_possible_web_menu_title">Authored heading</h2><p class="s_possible_web_menu_subtitle">Authored subtitle</p><div class="s_possible_web_menu_content is-loading" aria-busy="true"><div class="o_possible_web_menu_generated"><section class="o_possible_web_menu_category"><li class="o_possible_web_menu_product">Generated product <span class="o_possible_web_menu_price">CHF 9.95</span></li></section></div><p class="o_possible_web_menu_runtime_message">No products match.</p><p class="authored-content">Keep this authored content</p></div><p class="s_possible_web_menu_editor_warning">Runtime error</p></section>`;

describe("possible web menu builder cleanup", () => {
    test("cleans only the save clone and preserves authored configuration", () => {
        const fixture = getFixture();
        fixture.innerHTML = markup;
        const live = fixture.querySelector(".s_possible_web_menu");
        const clone = live.cloneNode(true);
        cleanPossibleWebMenuForSave(clone);
        expect(live.textContent.includes("Generated product")).toBe(true);
        expect(clone.querySelector(".o_possible_web_menu_generated")).toBe(null);
        expect(clone.querySelector(".o_possible_web_menu_runtime_message")).toBe(null);
        expect(clone.querySelector(".o_possible_web_menu_price")).toBe(null);
        expect(clone.querySelector(".s_possible_web_menu_content").classList.contains("is-loading")).toBe(false);
        expect(clone.querySelector(".s_possible_web_menu_content").getAttribute("aria-busy")).toBe("false");
        expect(clone.querySelector(".s_possible_web_menu_title").textContent).toBe("Authored heading");
        expect(clone.querySelector(".s_possible_web_menu_subtitle").textContent).toBe("Authored subtitle");
        expect(clone.dataset.pricelistId).toBe("7");
        expect(clone.dataset.layout).toBe("two_columns");
        expect(clone.querySelector(".authored-content").textContent).toBe("Keep this authored content");
    });
    test("cleans stale generated content from a duplicate without changing its configuration", () => {
        const fixture = getFixture();
        fixture.innerHTML = markup;
        const clone = fixture.querySelector(".s_possible_web_menu").cloneNode(true);
        cleanPossibleWebMenuForSave(clone);
        expect(clone.dataset.pricelistId).toBe("7");
        expect(clone.querySelector(".o_possible_web_menu_generated")).toBe(null);
    });
});
