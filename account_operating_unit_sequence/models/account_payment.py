# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models
from odoo.exceptions import UserError

MAP_SEQUENCE = {
    "customer": {
        "inbound": "payment_cust_inv_seq_id",
        "outbound": "payment_cust_refund_seq_id",
    },
    "supplier": {
        "inbound": "payment_supp_refund_seq_id",
        "outbound": "payment_supp_inv_seq_id",
    },
}


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def create(self, vals):
        if vals.get("operating_unit_id", False):
            ou = self.env["operating.unit"].browse(vals["operating_unit_id"])
            if vals["payment_type"] == "transfer":
                sequence_code = ou.payment_transfer_seq_id.code
            else:
                if vals["partner_type"] and vals["payment_type"]:
                    sequence_code = ou[
                        MAP_SEQUENCE[vals["partner_type"]][vals["payment_type"]]
                    ].code
            if sequence_code:
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    sequence_code, sequence_date=vals["payment_date"]
                )
        return super().create(vals)

    def post(self):
        if len(self.mapped("operating_unit_id")) != 1:
            raise UserError(
                _(
                    "The payment cannot be processed because "
                    "the operating units are different!"
                )
            )
        for rec in self:
            ou = rec.operating_unit_id
            if ou:
                # keep the name in case of a payment reset to draft
                if not rec.name:
                    # Use the right sequence to set the name
                    if rec.payment_type == "transfer":
                        sequence_code = ou.payment_transfer_seq_id.code
                    else:
                        if rec.partner_type and rec.payment_type:
                            sequence_code = ou[
                                MAP_SEQUENCE[rec.partner_type][rec.payment_type]
                            ].code
                    if sequence_code:
                        rec.name = self.env["ir.sequence"].next_by_code(
                            sequence_code, sequence_date=rec.payment_date
                        )
        return super().post()
