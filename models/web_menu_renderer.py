import re

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools import html2plaintext


class PossibleWebMenuRenderer(models.AbstractModel):
    _name = "possible.web.menu.renderer"
    _description = "POSsible Web Menu Renderer"

    _DEFAULTS = {"include_child_categories": True, "filter_sale": True, "filter_pos": True,
        "filter_purchase": False, "filter_mode": "all", "show_description": True,
        "show_internal_reference": False, "show_uncategorized": False, "tax_display": "included",
        "sort_mode": "favorite_ref_name", "layout": "leaders"}
    _ENUMS = {"filter_mode": {"all", "any"}, "tax_display": {"included", "excluded"},
              "sort_mode": {"favorite_ref_name", "pos_sequence_name", "name", "internal_reference"},
              "layout": {"leaders", "clean", "two_columns"}}

    @api.model
    def _normalize_config(self, values):
        result = dict(self._DEFAULTS)
        def boolean(value, default):
            if value is True or value == "true": return True
            if value is False or value == "false": return False
            return default
        try: pricelist_id = int(values.get("pricelist_id") or 0)
        except (TypeError, ValueError): pricelist_id = 0
        if pricelist_id < 1: raise ValidationError(_("A valid web-menu pricelist is required."))
        raw_ids = values.get("pos_category_ids") or []
        if isinstance(raw_ids, str): raw_ids = raw_ids.split(",") if raw_ids else []
        if not isinstance(raw_ids, (list, tuple)) or len(raw_ids) > 200: raise ValidationError(_("Invalid category selection."))
        try: category_ids = sorted({int(item) for item in raw_ids})
        except (TypeError, ValueError): raise ValidationError(_("Invalid category selection."))
        if any(item < 1 for item in category_ids): raise ValidationError(_("Invalid category selection."))
        result.update({"pricelist_id": pricelist_id, "pos_category_ids": category_ids})
        for key, default in self._DEFAULTS.items():
            if isinstance(default, bool): result[key] = boolean(values.get(key), default)
            elif values.get(key) in self._ENUMS[key]: result[key] = values[key]
        return result

    @api.model
    def _get_allowed_pricelist(self, config, website):
        pricelist = self.env["product.pricelist"].with_company(website.company_id).sudo().browse(config["pricelist_id"])
        if not pricelist.exists() or not pricelist.active or not pricelist.web_menu_available or (pricelist.company_id and pricelist.company_id != website.company_id):
            raise ValidationError(_("The selected pricelist is not available."))
        return pricelist

    @api.model
    def _get_category_scope(self, config):
        Category = self.env["pos.category"].sudo()
        ids = config["pos_category_ids"]
        if not ids: return Category
        domain = [("id", "child_of" if config["include_child_categories"] else "in", ids)]
        return Category.search(domain)

    @api.model
    def _build_product_domain(self, config, website, categories):
        domain = [("active", "=", True), ("web_menu_visible", "=", True), "|", ("company_id", "=", False), ("company_id", "=", website.company_id.id)]
        flags = [("sale_ok", "=", True), ("available_in_pos", "=", True), ("purchase_ok", "=", True)]
        selected = [item for item, enabled in zip(flags, (config["filter_sale"], config["filter_pos"], config["filter_purchase"])) if enabled]
        if selected:
            if config["filter_mode"] == "all": domain += selected
            else: domain += ["|"] * (len(selected) - 1) + selected
        if config["pos_category_ids"]: domain.append(("pos_categ_ids", "in", categories.ids))
        elif not config["show_uncategorized"]: domain.append(("pos_categ_ids", "!=", False))
        return domain

    @api.model
    def _get_products(self, config, website, categories):
        return self.env["product.template"].with_company(website.company_id).sudo().search(self._build_product_domain(config, website, categories))

    @api.model
    def _get_product_category(self, product, categories, config):
        candidates = product.pos_categ_ids if not categories else product.pos_categ_ids & categories
        if product.web_menu_category_id in candidates: return product.web_menu_category_id
        return candidates.sorted(lambda c: (c.sequence, c.name.casefold(), c.id))[:1]

    @api.model
    def _sort_products(self, products, mode):
        def key(product):
            name = (product.display_name or "").casefold(); ref = (product.default_code or "").casefold()
            if mode == "pos_sequence_name": return (product.pos_categ_ids[:1].sequence if product.pos_categ_ids else 0, name, product.id)
            if mode == "name": return (name, product.id)
            if mode == "internal_reference": return (not bool(ref), ref, name, product.id)
            return (not bool(product.is_favorite), not bool(ref), ref, name, product.id)
        return sorted(products, key=key)

    @api.model
    def _get_product_description(self, product):
        text = html2plaintext(product.web_menu_description or product.public_description or product.description_sale or "")
        return re.sub(r"\s+", " ", text).strip()

    @api.model
    def _compute_product_prices(self, products, pricelist, config, website):
        prices = pricelist._get_products_price(products, 1.0)
        result = {}
        for product in products:
            price = prices.get(product.id, prices.get(product, 0.0))
            taxes = product.taxes_id.filtered(lambda tax: not tax.company_id or tax.company_id == website.company_id)
            totals = taxes.compute_all(price, currency=pricelist.currency_id, quantity=1.0, product=product)
            result[product.id] = totals["total_included"] if config["tax_display"] == "included" else totals["total_excluded"]
        return result

    @api.model
    def _prepare_render_values(self, config, website):
        pricelist = self._get_allowed_pricelist(config, website)
        categories = self._get_category_scope(config)
        products = self._get_products(config, website, categories)
        prices = self._compute_product_prices(products, pricelist, config, website)
        grouped = {}; other = []
        for product in products:
            category = self._get_product_category(product, categories, config)
            if category: grouped.setdefault(category, []).append(product)
            elif not config["pos_category_ids"] and config["show_uncategorized"]: other.append(product)
        groups = [{"category": category, "products": self._sort_products(items, config["sort_mode"])} for category, items in sorted(grouped.items(), key=lambda it: (it[0].sequence, it[0].name.casefold(), it[0].id))]
        if other: groups.append({"category": False, "name": _("Other"), "products": self._sort_products(other, config["sort_mode"])})
        return {"groups": groups, "prices": prices, "currency": pricelist.currency_id, "config": config, "product_count": sum(len(g["products"]) for g in groups)}

    @api.model
    def _render_menu(self, config, website):
        values = self._prepare_render_values(config, website)
        html = self.env["ir.qweb"]._render("possible_web_menu.web_menu_fragment", values)
        return {"ok": True, "html": html, "product_count": values["product_count"], "category_count": len(values["groups"])}
