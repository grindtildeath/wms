# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from collections import defaultdict

from odoo.addons.component.core import Component
from odoo.tools import groupby


class ClusterPicking(Component):
    _inherit = "shopfloor.cluster.picking"

    def _lines_to_pick(self, picking_batch):
        breakpoint()
        res = super()._lines_to_pick(picking_batch)
        # if any(line.move_id.bom_line_id for line in res):
        #     for line in res:
        #         # TODO: Use float_compare
        #         # TODO: Handle UOM
        #         if line.move_id.product_uom_qty > line.move_id.bom_line_id.product_qty:
        #             # TODO: Split move line?
        #                      How to make sure move line is attached to correct move?!


            # for bom in res.move_id.bom_id:
                # move_lines_from_bom = res.filtered(lambda ml: ml.move_id.bom_line_id.bom_id == bom)
        # Split by bom line qty

        return res

    # def _use_package_from_last_picked_line(self, move_line, last_picked_line):
    #     # Suggest pack from last picked line only if 
    #     res = super()._use_package_from_last_picked_line(move_line, last_picked_line)
    #     # TODO: Add condition on  kit destination selection
    #     # if self.work.menu
    #     return res and move_line.move_id.bom_line_id.bom_id == last_picked_line.move_id.bom_line_id.bom_id

    # def scan_destination_pack(self, picking_batch_id, move_line_id, barcode, quantity):
    #     breakpoint()
    #     move_line = self.env["stock.move.line"].browse(move_line_id)
    #     last_picked_line = self._last_picked_line(move_line.picking_id)
    #     if self._use_package_from_last_picked_line() and barcode != last_picked_line.result_package_id.name:
    #         return self._response_for_scan_destination(
    #             move_line,
    #             message={
    #                 "message_type": "error",
    #                 "body": _(
    #                     "You must use the same package as the last move line: {}"
    #                 ).format(last_picked_line.result_package_id.name),
    #             },
    #             qty_done=quantity,
    #         )
    #     return super().scan_destination_pack(picking_batch_id, move_line_id, barcode, quantity)

    def _pre_pick_batch_hook(self, batch):
        kit_package_mapping = {}
        if self.work.menu.destination_package_selection == "predefined" and self.work.menu.force_kit_pacakge_ids and not all(ml.result_package_id for ml in batch.picking_ids.move_line_ids):
            for picking in batch.picking_ids:
                # TODO: Consider components with tracking?
                for bom, bom_moves_list in groupby(
                    picking.move_lines.filtered(lambda ml: ml.bom_line_id.bom_id.type == "phantom"),
                    lambda ml: ml.bom_line_id.bom_id
                ):
                    product_id_moves_ids_dict = defaultdict(list)
                    moves = self.env["stock.move"].browse([move.id for move in bom_moves_list])
                    # TODO: Check if this is right
                    filters = {"incoming_moves": lambda m: True, "outgoing_moves": lambda m: False}
                    kit_quantity = moves._compute_kit_quantities(bom.product_id, max(moves.mapped("product_qty")), bom, filters)
                    # TODO: Use abs() and/or float_compare?
                    if kit_quantity > 1.0:
                        for move in moves:
                            move._do_unreserve()
                            product_id_moves_ids_dict[move.product_id.id].append(move.id)
                            new_moves_values = []
                            for kit_piece in range(int(kit_quantity) - 1):
                                new_move_values = move._split(move.bom_line_id.product_qty)
                                new_moves_values.append(new_move_values)
                            new_moves = self.env["stock.move"].create(new_move_values)
                            product_id_moves_ids_dict[move.product_id.id].extend(new_moves.ids)
                    for product_id, moves_ids in product_id_moves_ids_dict.items():
                        moves = self.env["stock.move"].browse(moves_ids)
                        moves._action_assign()
                        for move, kit_package in zip(moves, self.work.menu.force_kit_pacakge_ids):
                            move.move_line_ids.write({"result_package_id": kit_package.package_id.id})
        return super()._pre_pick_batch_hook(batch)
