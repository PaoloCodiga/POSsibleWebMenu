/** @odoo-module **/
import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { normalizeDataset, payloadFromConfig } from "./possible_web_menu_utils";

export class PossibleWebMenuInteraction extends Interaction {
    static selector = ".s_possible_web_menu";
    setup() { this.generation = 0; this.observer = new MutationObserver(() => this.debouncedRefresh()); this.observer.observe(this.el, {attributes: true, attributeFilter: ["data-pricelist-id", "data-pos-category-ids", "data-include-child-categories", "data-filter-sale", "data-filter-pos", "data-filter-purchase", "data-filter-mode", "data-show-description", "data-show-internal-reference", "data-show-uncategorized", "data-tax-display", "data-sort-mode", "data-layout"]}); }
    willStart() { return this.refresh(); }
    destroy() { this.observer?.disconnect(); clearTimeout(this.timer); super.destroy(); }
    debouncedRefresh() { clearTimeout(this.timer); this.timer = setTimeout(() => this.refresh(), 100); }
    async refresh() { const config=normalizeDataset(this.el.dataset), content=this.el.querySelector(".s_possible_web_menu_content"), warning=this.el.querySelector(".s_possible_web_menu_editor_warning"); if (!config.pricelistId) { content.replaceChildren(); warning?.classList.add("d-none"); return; } warning?.classList.add("d-none"); const generation=++this.generation; content.setAttribute("aria-busy", "true"); try { const response=await this.services.rpc("/possible_web_menu/render", payloadFromConfig(config)); if (!this.isDestroyed && generation === this.generation && response.ok) content.innerHTML=response.html; } catch { if (!this.isDestroyed && generation === this.generation) content.replaceChildren(); } finally { if (!this.isDestroyed && generation === this.generation) content.setAttribute("aria-busy", "false"); } }
}
registry.category("public.interactions").add("possible_web_menu", PossibleWebMenuInteraction);
