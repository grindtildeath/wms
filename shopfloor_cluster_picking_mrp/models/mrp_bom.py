# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    avoid_merging_operations_by_unit = fields.Boolean()