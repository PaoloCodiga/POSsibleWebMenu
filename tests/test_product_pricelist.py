from odoo.tests import tagged

from .common import WebMenuCase


@tagged("post_install", "-at_install", "possible_web_menu")
class TestProductPricelist(WebMenuCase):
    def test_availability_default_and_copy(self):
        pricelist = self.env["product.pricelist"].create({"name": "Web menu test pricelist"})
        self.assertFalse(pricelist.web_menu_available)
        pricelist.web_menu_available = True
        self.assertFalse(pricelist.copy().web_menu_available)
