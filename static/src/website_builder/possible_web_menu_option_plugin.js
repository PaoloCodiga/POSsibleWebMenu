/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { BaseOptionComponent } from "@html_builder/core/utils";
import { BuilderAction } from "@html_builder/core/builder_action";
import { before, SNIPPET_SPECIFIC_END } from "@html_builder/utils/option_sequence";
import { withSequence } from "@html_editor/utils/resource";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { normalizeDataset } from "@possible_web_menu/snippets/s_possible_web_menu/possible_web_menu_utils";
import { PossibleWebMenuConfigurationDialog } from "./possible_web_menu_configuration_dialog";

export class PossibleWebMenuOption extends BaseOptionComponent {
    static template = "possible_web_menu.Option";
    static selector = ".s_possible_web_menu";

    setup() {
        super.setup();
        this.dialog = useService("dialog");
    }

    openConfigurationDialog() {
        const snippet = this.env.getEditingElement()?.closest(this.constructor.selector);
        if (!snippet) {
            return;
        }
        this.dialog.add(PossibleWebMenuConfigurationDialog, {
            applyConfiguration: (configuration) => this.applyConfiguration(snippet, configuration),
            configuration: normalizeDataset(snippet.dataset),
        });
    }

    applyConfiguration(snippet, configuration) {
        this.env.editor.shared.builderActions.applyAction("applyPossibleWebMenuConfiguration", {
            editingElement: snippet,
            value: configuration,
        });
    }
}

export class ApplyPossibleWebMenuConfiguration extends BuilderAction {
    static id = "applyPossibleWebMenuConfiguration";

    apply({ editingElement, value }) {
        const configuration = normalizeDataset({
            configVersion: value.configVersion,
            pricelistId: value.pricelistId,
            posCategoryIds: value.posCategoryIds.join(","),
            includeChildCategories: value.includeChildCategories,
            filterSale: value.filterSale,
            filterPos: value.filterPos,
            filterPurchase: value.filterPurchase,
            filterMode: value.filterMode,
            showDescription: value.showDescription,
            showInternalReference: value.showInternalReference,
            showUncategorized: value.showUncategorized,
            taxDisplay: value.taxDisplay,
            sortMode: value.sortMode,
            layout: value.layout,
        });
        if (!configuration.pricelistId) {
            return;
        }
        Object.assign(editingElement.dataset, {
            configVersion: configuration.configVersion,
            pricelistId: String(configuration.pricelistId),
            posCategoryIds: configuration.posCategoryIds.join(","),
            includeChildCategories: String(configuration.includeChildCategories),
            filterSale: String(configuration.filterSale),
            filterPos: String(configuration.filterPos),
            filterPurchase: String(configuration.filterPurchase),
            filterMode: configuration.filterMode,
            showDescription: String(configuration.showDescription),
            showInternalReference: String(configuration.showInternalReference),
            showUncategorized: String(configuration.showUncategorized),
            taxDisplay: configuration.taxDisplay,
            sortMode: configuration.sortMode,
            layout: configuration.layout,
        });
        return this.dispatchTo("update_interactions", editingElement);
    }
}

export function cleanPossibleWebMenuForSave(root) {
    const snippets = [
        ...(root.matches?.(".s_possible_web_menu") ? [root] : []),
        ...root.querySelectorAll(".s_possible_web_menu"),
    ];
    for (const snippet of snippets) {
        const content = snippet.querySelector(".s_possible_web_menu_content");
        content?.querySelectorAll(".o_possible_web_menu_generated, .o_possible_web_menu_runtime_message").forEach((element) => element.remove());
        content?.classList.remove("is-loading", "o_possible_web_menu_loading", "o_possible_web_menu_error");
        content?.setAttribute("aria-busy", "false");
        snippet.querySelectorAll(".s_possible_web_menu_editor_warning").forEach((element) => {
            element.textContent = "";
            element.classList.add("d-none");
        });
    }
}

export class PossibleWebMenuOptionPlugin extends Plugin {
    static id = "possibleWebMenuOptionPlugin";
    resources = {
        builder_options: [withSequence(before(SNIPPET_SPECIFIC_END), PossibleWebMenuOption)],
        builder_actions: { ApplyPossibleWebMenuConfiguration },
        clean_for_save_handlers: [({ root }) => cleanPossibleWebMenuForSave(root)],
        on_cloned_handlers: ({ cloneEl }) => cleanPossibleWebMenuForSave(cloneEl),
    };
}

registry.category("website-plugins").add(PossibleWebMenuOptionPlugin.id, PossibleWebMenuOptionPlugin);
