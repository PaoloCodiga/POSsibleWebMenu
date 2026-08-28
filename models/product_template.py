from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    web_menu_visible = fields.Boolean(string="Visible in Web Menu", default=False, copy=False, index=True)
    web_menu_category_id = fields.Many2one(
        "pos.category", string="Primary Web Menu Category", ondelete="set null", index=True,
        domain="[('id', 'in', pos_categ_ids)]",
    )

    @api.constrains("web_menu_category_id", "pos_categ_ids")
    def _check_web_menu_category(self):
        for product in self:
            if product.web_menu_category_id and product.web_menu_category_id not in product.pos_categ_ids:
                raise ValidationError(_("The primary web menu category must be one of the POS categories."))

    @api.onchange("pos_categ_ids")
    def _onchange_pos_categ_ids_web_menu_category(self):
        if self.web_menu_category_id and self.web_menu_category_id not in self.pos_categ_ids:
            self.web_menu_category_id = False

    def action_enable_web_menu(self):
        self.write({"web_menu_visible": True})

    def action_disable_web_menu(self):
        self.write({"web_menu_visible": False})
