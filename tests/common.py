from odoo.tests.common import TransactionCase


class WebMenuCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.category = cls.env["pos.category"].create({"name": "Web menu test category"})
        cls.product = cls.env["product.template"].create({
            "name": "Web menu test product",
            "sale_ok": True,
            "available_in_pos": True,
            "pos_categ_ids": [(6, 0, cls.category.ids)],
        })
