from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError


class PossibleWebMenuController(http.Controller):
    @http.route("/possible_web_menu/render", type="jsonrpc", auth="public", website=True, methods=["POST"], readonly=True)
    def render(self, pricelist_id=None, pos_category_ids=None, include_child_categories=None, filter_sale=None, filter_pos=None, filter_purchase=None, filter_mode=None, show_description=None, show_internal_reference=None, show_uncategorized=None, tax_display=None, sort_mode=None, layout=None):
        values = locals().copy(); values.pop("self")
        try:
            config = request.env["possible.web.menu.renderer"]._normalize_config(values)
            return request.env["possible.web.menu.renderer"]._render_menu(config, request.website)
        except (ValidationError, ValueError, TypeError):
            return {"ok": False, "html": "", "product_count": 0, "category_count": 0, "error_code": "invalid_configuration"}

    @http.route("/possible_web_menu/builder/options", type="jsonrpc", auth="user", website=True, methods=["POST"], readonly=True)
    def builder_options(self):
        if not request.env.user.has_group("website.group_website_designer"):
            raise AccessError("Website editor access is required.")
        website = request.website
        Pricelist = request.env["product.pricelist"].with_company(website.company_id).sudo()
        pricelists = Pricelist.search([("active", "=", True), ("web_menu_available", "=", True), "|", ("company_id", "=", False), ("company_id", "=", website.company_id.id)])
        categories = request.env["pos.category"].sudo().search([], order="sequence, name, id")
        return {"pricelists": [{"id": p.id, "name": p.name, "currency": p.currency_id.name} for p in pricelists], "categories": [{"id": c.id, "name": c.name, "parent_id": c.parent_id.id or False, "sequence": c.sequence} for c in categories]}
