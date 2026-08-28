from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    web_menu_available = fields.Boolean(string="Available in Web Menu", default=False, copy=False, index=True)
