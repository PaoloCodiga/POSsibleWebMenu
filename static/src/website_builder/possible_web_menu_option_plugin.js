/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";

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
        clean_for_save_handlers: [({ root }) => cleanPossibleWebMenuForSave(root)],
        on_cloned_handlers: ({ cloneEl }) => cleanPossibleWebMenuForSave(cloneEl),
    };
}

registry.category("website-plugins").add(PossibleWebMenuOptionPlugin.id, PossibleWebMenuOptionPlugin);
