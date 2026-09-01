/** @odoo-module **/

import { describe, expect, getFixture, test } from "@odoo/hoot";
import { queryOne } from "@odoo/hoot-dom";
import { rpc } from "@web/core/network/rpc";

import { PossibleWebMenuInteraction } from "@possible_web_menu/snippets/s_possible_web_menu/possible_web_menu";

const snippet = (pricelistId = "7") => /* xml */ `
    <section class="s_possible_web_menu"
        data-pricelist-id="${pricelistId}"
        data-pos-category-ids="4,2,4"
        data-include-child-categories="true"
        data-filter-sale="true"
        data-filter-pos="true"
        data-filter-purchase="false"
        data-filter-mode="all"
        data-show-description="true"
        data-show-internal-reference="false"
        data-show-uncategorized="false"
        data-tax-display="included"
        data-sort-mode="favorite_ref_name"
        data-layout="leaders">
        <div class="s_possible_web_menu_content" aria-busy="false"></div>
        <p class="s_possible_web_menu_editor_warning d-none" data-warning="configure">Configure this menu to preview products.</p>
        <p class="s_possible_web_menu_editor_warning d-none" data-warning="empty">No products match this menu configuration.</p>
        <p class="s_possible_web_menu_editor_warning d-none" data-warning="failure">The menu preview is temporarily unavailable.</p>
    </section>`;

async function startMenuInteraction(html, rpcHandler) {
    const fixture = getFixture();
    fixture.innerHTML = html;
    const originalRpc = rpc._rpc;
    rpc._rpc = rpcHandler;
    const interaction = new PossibleWebMenuInteraction(
        queryOne(".s_possible_web_menu"),
        { services: {} },
        { isDestroyed: false }
    );

    try {
        interaction.setup();
        await interaction.willStart();
    } finally {
        rpc._rpc = originalRpc;
    }
    return interaction;
}

describe("possible web menu public interaction", () => {
    test("renders the public QWeb response for a configured snippet", async () => {
        const calls = [];
        await startMenuInteraction(snippet(), async (route, payload) => {
            calls.push({ route, payload });
            return { ok: true, html: '<div class="o_possible_web_menu">Rendered menu</div>' };
        });

        expect(calls).toEqual([
            {
                route: "/possible_web_menu/render",
                payload: {
                pricelist_id: 7,
                pos_category_ids: [2, 4],
                include_child_categories: true,
                filter_sale: true,
                filter_pos: true,
                filter_purchase: false,
                filter_mode: "all",
                show_description: true,
                show_internal_reference: false,
                show_uncategorized: false,
                tax_display: "included",
                sort_mode: "favorite_ref_name",
                layout: "leaders",
                },
            },
        ]);

        expect(queryOne(".s_possible_web_menu_content").textContent).toBe("Rendered menu");
        expect(queryOne(".s_possible_web_menu_content")).toHaveAttribute("aria-busy", "false");
        expect(queryOne('[data-warning="configure"]')).toHaveClass("d-none");
    });

    test("does not call the public route without a pricelist", async () => {
        let calls = 0;
        await startMenuInteraction(snippet(""), async () => {
            calls += 1;
            return { ok: true, html: "Unexpected response" };
        });

        expect(calls).toBe(0);
        expect(queryOne(".s_possible_web_menu_content")).toHaveText("");
    });

    test("shows empty and failure feedback only in the editor", async () => {
        const fixture = getFixture();
        fixture.innerHTML = snippet();
        const root = queryOne(".s_possible_web_menu");
        root.classList.add("o_editable");
        const originalRpc = rpc._rpc;
        rpc._rpc = async () => ({ ok: true, html: "", product_count: 0 });
        const empty = new PossibleWebMenuInteraction(root, { services: {} }, { isDestroyed: false });
        try {
            empty.setup();
            await empty.willStart();
        } finally {
            rpc._rpc = originalRpc;
        }
        expect(queryOne('[data-warning="empty"]')).not.toHaveClass("d-none");

        rpc._rpc = async () => ({ ok: false, html: "", product_count: 0 });
        const failure = new PossibleWebMenuInteraction(root, { services: {} }, { isDestroyed: false });
        try {
            failure.setup();
            await failure.willStart();
        } finally {
            rpc._rpc = originalRpc;
        }
        expect(queryOne('[data-warning="failure"]')).not.toHaveClass("d-none");
    });
});
