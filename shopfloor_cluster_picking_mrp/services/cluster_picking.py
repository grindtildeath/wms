# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from collections import defaultdict

from odoo.addons.component.core import Component
from odoo.tools import float_compare, groupby


class ClusterPicking(Component):
    _inherit = "shopfloor.cluster.picking"

    def _pre_pick_batch_hook(self, batch):
        if self.work.menu.destination_package_selection == "predefined" and self.work.menu.force_kit_pacakge_ids and not all(ml.result_package_id for ml in batch.picking_ids.move_line_ids):
            for picking in batch.picking_ids:
                for bom, bom_moves_list in groupby(
                    picking.move_lines.filtered(lambda ml: ml.bom_line_id.bom_id.type == "phantom"),
                    lambda ml: ml.bom_line_id.bom_id
                ):
                    moves = self.env["stock.move"].browse([move.id for move in bom_moves_list])
                    filters = {"incoming_moves": lambda m: True, "outgoing_moves": lambda m: False}
                    kit_quantity = moves._compute_kit_quantities(bom.product_id, max(moves.mapped("product_qty")), bom, filters)
                    # TODO: Use abs(kit_quantity)?
                    if float_compare(kit_quantity, 1.0, precision, precision_rounding=bom.product_id.uom_id.rounding) >= 0:
                        for move in moves.filtered(lambda m: m.product_id.tracking != "serial"):
                            # TODO: Handle possibility of having more than one move line in case
                            #  product is tracked by lots and we have multiple lots assigned?
                            existing_line = move.move_line_ids
                            move_lines_values_list = []
                            for kit_piece in range(int(kit_quantity) - 1):
                                # TODO: Handle UOM?
                                move_lines_values_list.extend(
                                    existing_line.copy_data({"product_uom_qty": move.bom_line_id.product_qty})
                                )
                            # Update existing move line quantity and add new move lines without changing reservation
                            move.with_context(**dict(do_not_unreserve=True, bypass_reservation_update=True)).write(
                                {
                                    "move_line_ids": [
                                        (1, existing_line.id, {"product_uom_qty": move.bom_line_id.product_qty})
                                    ] + [
                                        (0, 0, vals) for vals in move_lines_values_list
                                    ]
                                }
                            )
                            for move_line, kit_package in zip(move.move_line_ids, self.work.menu.force_kit_pacakge_ids):
                                move_line.write({"result_package_id": kit_package.package_id.id})
                        for move in moves.filtered(lambda m: m.product_id.tracking == "serial"):
                            # TODO: Add check in case we don't have serial number assigned?
                            # Here we assume we have as many move lines as the total quantity on the move
                            for kit_package in self.work.menu.force_kit_pacakge_ids:
                                step = move.bom_line_id.product_qty
                                for cnt in range(0, move.product_uom_qty, step):
                                    lines = move.move_line_ids[cnt : cnt + step - 1]
                                    lines.write({"result_package_id": kit_package.package_id.id})
        return super()._pre_pick_batch_hook(batch)
