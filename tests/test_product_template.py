from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import WebMenuCase


@tagged("post_install", "-at_install", "possible_web_menu")
class TestProductTemplate(WebMenuCase):
    def test_visibility_default_and_copy(self):
        self.assertFalse(self.product.web_menu_visible)
        self.product.web_menu_visible = True
        self.assertFalse(self.product.copy().web_menu_visible)

    def test_primary_category_constraint_and_onchange(self):
        other = self.env["pos.category"].create({"name": "Other category"})
        self.product.web_menu_category_id = self.category
        with self.assertRaises(ValidationError):
            self.product.write({"web_menu_category_id": other.id})
        draft = self.env["product.template"].new({
            "name": "Onchange product",
            "pos_categ_ids": [(6, 0, self.category.ids)],
            "web_menu_category_id": self.category.id,
        })
        draft.pos_categ_ids = [(5, 0, 0)]
        draft._onchange_pos_categ_ids_web_menu_category()
        self.assertFalse(draft.web_menu_category_id)

    def test_bulk_actions(self):
        self.product.action_enable_web_menu()
        self.assertTrue(self.product.web_menu_visible)
        self.product.action_disable_web_menu()
        self.assertFalse(self.product.web_menu_visible)
