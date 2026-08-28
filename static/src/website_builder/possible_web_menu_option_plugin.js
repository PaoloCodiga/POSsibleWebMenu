/** @odoo-module **/
import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";
export class PossibleWebMenuOptionPlugin extends Plugin { static id = "possibleWebMenuOptionPlugin"; resources = { clean_for_save_handlers: [({root}) => root.querySelectorAll(".s_possible_web_menu_content").forEach((el) => el.replaceChildren())] }; }
registry.category("website-plugins").add(PossibleWebMenuOptionPlugin.id, PossibleWebMenuOptionPlugin);
