# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    # kit_unit_identifier = fields.Char()

    # @api.model
    # def _prepare_merge_moves_distinct_fields(self):
    #     distinct_fields = super()._prepare_merge_moves_distinct_fields()
    #     if self.bom_line_id and ("phantom" in self.bom_line_id.bom_id.mapped('type')):
    #         distinct_fields.append("kit_unit_identifier")
    #     return distinct_fields

    # def action_explode(self):
    #     existing_moves = self
    #     kit_quantities = {}
    #     for move in self:
    #         bom = self.env['mrp.bom'].sudo()._bom_find(product=move.product_id, company_id=move.company_id.id, bom_type='phantom')
    #         if not bom.avoid_merging_operations_by_unit:
    #             continue
    #         # TODO: Handle UOM?
    #         kit_quantities[move.product_id] = move.product_uom_qty
    #     res = super().action_explode()
    #     for kit_product, quantity in kit_quantities.items():
    #         for phantom_move in res.filtered(lambda m: m.id not in existing_moves.ids):
                

    #     return res
