import json

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install", "possible_web_menu")
class TestPossibleWebMenuBuilderOptions(HttpCase):
    def test_builder_options_return_allowed_pricelists_and_category_hierarchy(self):
        website = self.env["website"].get_current_website()
        pricelist = self.env["product.pricelist"].create({
            "name": "C1 Builder Pricelist",
            "active": True,
            "web_menu_available": True,
            "company_id": website.company_id.id,
        })
        parent_category = self.env["pos.category"].create({"name": "C1 Parent", "sequence": 4})
        child_category = self.env["pos.category"].create({
            "name": "C1 Child",
            "parent_id": parent_category.id,
            "sequence": 5,
        })

        self.authenticate("admin", "admin")
        response = self.url_open(
            "/possible_web_menu/builder/options",
            json={"params": {}},
        )
        result = json.loads(response.content)["result"]

        returned_pricelist = next(
            item for item in result["pricelists"] if item["id"] == pricelist.id
        )
        returned_child_category = next(
            item for item in result["categories"] if item["id"] == child_category.id
        )
        self.assertEqual(returned_pricelist["name"], pricelist.name)
        self.assertEqual(returned_pricelist["currency"], pricelist.currency_id.name)
        self.assertEqual(returned_pricelist["currency_symbol"], pricelist.currency_id.symbol)
        self.assertEqual(returned_child_category["parent_id"], parent_category.id)
        self.assertEqual(returned_child_category["sequence"], child_category.sequence)
        self.assertEqual(returned_child_category["depth"], 1)
