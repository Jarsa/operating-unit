# Copyright 2023 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class StockLocationRoute(models.Model):
    _inherit = "stock.location.route"

    operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
        string="Operating Units",
    )
