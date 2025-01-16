# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Shopfloor Cluster Picking MRP",
    "summary": "Module summary",  # TODO
    "version": "14.0.1.0.0",
    "development_status": "Alpha",
    "category": "Inventory",
    "website": "https://github.com/OCA/wms",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "shopfloor",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/shopfloor_menu.xml",
    ],
}
