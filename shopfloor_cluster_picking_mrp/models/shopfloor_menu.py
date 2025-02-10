# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ShopfloorMenu(models.Model):
    _inherit = "shopfloor.menu"

    # FIXME: Remove typo
    force_kit_pacakge_ids = fields.One2many("shopfloor.menu.force.package", "menu_id", string="Force kit into package on batch creation")


class ShopfloorMenuForcePackage(models.Model):
    _name = "shopfloor.menu.force.package"
    _description = "Packages to force when processing"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    menu_id = fields.Many2one("shopfloor.menu", required=True)
    package_id = fields.Many2one("stock.quant.package", required=True)
