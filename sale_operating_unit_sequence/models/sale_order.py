# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        if vals.get("operating_unit_id", False):
            seq_date = None
            if "date_order" in vals:
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals["date_order"])
                )
            sequence_code = (
                self.env["operating.unit"]
                .browse(vals["operating_unit_id"])
                .sale_sequence_id.code
            )
            if sequence_code:
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    sequence_code, sequence_date=seq_date
                )
        return super().create(vals)
