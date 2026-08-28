from odoo.tests import tagged

from .common import WebMenuCase


@tagged("post_install", "-at_install", "possible_web_menu")
class TestRendererDomain(WebMenuCase):
    def test_mandatory_public_eligibility_domain(self):
        renderer = self.env["possible.web.menu.renderer"]
        config = renderer._normalize_config({"pricelist_id": 1, "pos_category_ids": []})
        domain = renderer._build_product_domain(config, self.env["website"].get_current_website(), self.env["pos.category"])
        self.assertIn(("active", "=", True), domain)
        self.assertIn(("web_menu_visible", "=", True), domain)
        self.assertIn(("sale_ok", "=", True), domain)
        self.assertIn(("available_in_pos", "=", True), domain)

    def test_no_optional_filter_and_selected_category_scope(self):
        renderer = self.env["possible.web.menu.renderer"]
        config = renderer._normalize_config({"pricelist_id": 1, "pos_category_ids": [self.category.id], "filter_sale": False, "filter_pos": False, "filter_purchase": False})
        domain = renderer._build_product_domain(config, self.env["website"].get_current_website(), self.category)
        self.assertNotIn(("sale_ok", "=", True), domain)
        self.assertIn(("pos_categ_ids", "in", self.category.ids), domain)
