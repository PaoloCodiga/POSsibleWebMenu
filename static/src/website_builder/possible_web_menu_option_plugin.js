/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { BaseOptionComponent } from "@html_builder/core/utils";
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
            configuration: normalizeDataset(snippet.dataset),
        });
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
        clean_for_save_handlers: [({ root }) => cleanPossibleWebMenuForSave(root)],
        on_cloned_handlers: ({ cloneEl }) => cleanPossibleWebMenuForSave(cloneEl),
    };
}

registry.category("website-plugins").add(PossibleWebMenuOptionPlugin.id, PossibleWebMenuOptionPlugin);
