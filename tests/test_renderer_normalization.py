from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import WebMenuCase


@tagged("post_install", "-at_install", "possible_web_menu")
class TestRendererNormalization(WebMenuCase):
    def test_normalizes_explicit_values_only(self):
        renderer = self.env["possible.web.menu.renderer"]
        config = renderer._normalize_config({
            "pricelist_id": "7", "pos_category_ids": "3,2,3", "filter_sale": "false",
            "filter_mode": "bad", "layout": "two_columns", "domain": [("name", "=", "unsafe")],
        })
        self.assertEqual(config["pricelist_id"], 7)
        self.assertEqual(config["pos_category_ids"], [2, 3])
        self.assertFalse(config["filter_sale"])
        self.assertEqual(config["filter_mode"], "all")
        self.assertEqual(config["layout"], "two_columns")
        self.assertNotIn("domain", config)

    def test_rejects_missing_or_invalid_ids(self):
        renderer = self.env["possible.web.menu.renderer"]
        with self.assertRaises(ValidationError): renderer._normalize_config({"pricelist_id": 0})
        with self.assertRaises(ValidationError): renderer._normalize_config({"pricelist_id": 1, "pos_category_ids": [-1]})
        with self.assertRaises(ValidationError): renderer._normalize_config({"pricelist_id": 1, "pos_category_ids": list(range(201))})
