/** @odoo-module **/
import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { normalizeDataset, payloadFromConfig } from "./possible_web_menu_utils";

export class PossibleWebMenuInteraction extends Interaction {
    static selector = ".s_possible_web_menu";

    setup() {
        this.generation = 0;
    }

    willStart() {
        return this.refresh();
    }

    destroy() {
        this.generation += 1;
        super.destroy();
    }

    async refresh() {
        const content = this.el.querySelector(".s_possible_web_menu_content");
        const config = normalizeDataset(this.el.dataset);

        this._hideEditorWarning();
        if (!content || !config.pricelistId) {
            content?.replaceChildren();
            this._showEditorWarning("configure");
            return;
        }

        const generation = ++this.generation;
        content.setAttribute("aria-busy", "true");
        try {
            const response = await rpc(
                "/possible_web_menu/render",
                payloadFromConfig(config)
            );
            if (!this.isDestroyed && generation === this.generation) {
                if (response.ok) {
                    content.innerHTML = `<div class="o_possible_web_menu_generated">${response.html}</div>`;
                } else {
                    content.replaceChildren();
                    this._showEditorWarning("failure");
                }
                if (response.ok && !response.product_count) this._showEditorWarning("empty");
            }
        } catch {
            if (!this.isDestroyed && generation === this.generation) {
                content.replaceChildren();
                this._showEditorWarning("failure");
            }
        } finally {
            if (!this.isDestroyed && generation === this.generation) {
                content.setAttribute("aria-busy", "false");
            }
        }
    }

    _isEditorMode() {
        return Boolean(this.el.closest(".o_editable")) || this.el.ownerDocument.body.classList.contains("editor_enable");
    }

    _hideEditorWarning() {
        this.el.querySelectorAll(".s_possible_web_menu_editor_warning").forEach((warning) => warning.classList.add("d-none"));
    }

    _showEditorWarning(kind) {
        if (this._isEditorMode()) this.el.querySelector(`.s_possible_web_menu_editor_warning[data-warning="${kind}"]`)?.classList.remove("d-none");
    }
}
registry.category("public.interactions").add("possible_web_menu", PossibleWebMenuInteraction);
registry.category("public.interactions.edit").add("possible_web_menu", {
    Interaction: PossibleWebMenuInteraction,
});
registry.category("public.interactions.preview").add("possible_web_menu", {
    Interaction: PossibleWebMenuInteraction,
});
