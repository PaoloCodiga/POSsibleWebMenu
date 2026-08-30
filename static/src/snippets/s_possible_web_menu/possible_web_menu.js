/** @odoo-module **/
import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
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
        const warning = this.el.querySelector(".s_possible_web_menu_editor_warning");
        const config = normalizeDataset(this.el.dataset);

        warning?.classList.add("d-none");
        if (!content || !config.pricelistId) {
            content?.replaceChildren();
            return;
        }

        const generation = ++this.generation;
        content.setAttribute("aria-busy", "true");
        try {
            const response = await this.services.rpc(
                "/possible_web_menu/render",
                payloadFromConfig(config)
            );
            if (!this.isDestroyed && generation === this.generation) {
                if (response.ok) {
                    content.innerHTML = response.html;
                } else {
                    content.replaceChildren();
                }
            }
        } catch {
            if (!this.isDestroyed && generation === this.generation) {
                content.replaceChildren();
            }
        } finally {
            if (!this.isDestroyed && generation === this.generation) {
                content.setAttribute("aria-busy", "false");
            }
        }
    }
}
registry.category("public.interactions").add("possible_web_menu", PossibleWebMenuInteraction);
