# Copyright 2023 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "Stock Location Route Operating Unit",
    "summary": "Manage Operating Unit in Stock Routes",
    "version": "15.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "Inventory/Inventory",
    "website": "https://github.com/OCA/operating-unit",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "maintainers": ["alan196"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_stock_operating_unit",
    ],
    "data": [
        "views/stock_location_route_view.xml",
        "views/sale_order_view.xml",
    ],
}
